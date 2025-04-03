from datetime import datetime
from typing import cast

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import StreamWriter

from onyx.agents.agent_search.dc_search_analysis.ops import research
from onyx.agents.agent_search.dc_search_analysis.states import MainState
from onyx.agents.agent_search.dc_search_analysis.states import (
    SearchSourcesObjectsUpdate,
)
from onyx.agents.agent_search.models import GraphConfig
from onyx.agents.agent_search.shared_graph_utils.utils import write_custom_event
from onyx.chat.models import AgentAnswerPiece
from onyx.configs.constants import DocumentSource
from onyx.prompts.kg_prompts import DC_OBJECT_NO_BASE_DATA_EXTRACTION_PROMPT
from onyx.prompts.kg_prompts import DC_OBJECT_WITH_BASE_DATA_EXTRACTION_PROMPT
from onyx.utils.logger import setup_logger
from onyx.utils.threadpool_concurrency import run_with_timeout

logger = setup_logger()


def search_objects(
    state: MainState, config: RunnableConfig, writer: StreamWriter = lambda _: None
) -> SearchSourcesObjectsUpdate:
    """
    LangGraph node to start the agentic search process.
    """
    datetime.now()

    graph_config = cast(GraphConfig, config["metadata"]["config"])
    question = graph_config.inputs.search_request.query
    search_tool = graph_config.tooling.search_tool

    if search_tool is None or graph_config.inputs.search_request.persona is None:
        raise ValueError("search tool and persona must be provided for agentic search")

    try:
        instructions = graph_config.inputs.search_request.persona.prompts[
            0
        ].system_prompt

        if "|Start Data|" and "|End Data|" in instructions:
            agent_1_base_data = instructions.split("|Start Data|")[1].split(
                "|End Data|"
            )[0]
        else:
            agent_1_base_data = None

        agent_1_instructions = instructions.split("Agent Step 1:")[1].split(
            "Agent Step 2:"
        )[0]

        agent_1_task = agent_1_instructions.split("Task:")[1].split(
            "Independent Sources:"
        )[0]
        agent_1_independent_sources_str = agent_1_instructions.split(
            "Independent Sources:"
        )[1].split("Output Objective:")[0]
        document_sources = [
            DocumentSource(x.strip().lower())
            for x in agent_1_independent_sources_str.split(";")
        ]
        agent_1_output_objective = agent_1_instructions.split("Output Objective:")[1]
    except Exception as e:
        raise ValueError(
            f"Agent 1 instructions not found or not formatted correctly: {e}"
        )

    # Extract objects

    if agent_1_base_data is None:
        # Retrieve chunks for objects

        retrieved_docs = research(question, search_tool)[:10]
        # aaa = (x for x in retrieved_docs.top_sections[:10])
        # retrieved_inference_sections = [inference_section_from_llm_doc(llm_doc)
        #                                for llm_doc in retrieved_docs]

        # yield ToolResponse(id=FINAL_CONTEXT_DOCUMENTS_ID, response=retrieved_docs)

        # aaa = yield_search_responses(
        #     query=question,
        #     get_retrieved_sections=lambda: retrieved_inference_sections,
        #     get_final_context_sections=lambda: retrieved_inference_sections[:10],
        #     search_query_info=SearchQueryInfo(
        #         predicted_search=SearchType.SEMANTIC,
        #         final_filters=IndexFilters(access_control_list=None),
        #         recency_bias_multiplier=1.0,
        #     ),
        #     get_section_relevance=lambda: None,
        #     search_tool=search_tool,
        # )

        # for aa in aaa:

        #     write_custom_event(
        #             "tool_response",
        #             ToolResponse(
        #                 id=SEARCH_RESPONSE_SUMMARY_ID,
        #                 response=aa,
        #             ),
        #             writer,
        #         )

        # write_custom_event(
        #     "initial_agent_answer",
        #     AgentAnswerPiece(
        #         answer_piece="Identifying the [[7]] appropriate objects...",
        #         level=0,
        #         level_question_num=0,
        #         answer_type="agent_level_answer",
        #     ),
        #     writer,
        # )
        # # Generate document text

        document_texts_list = []
        for doc_num, doc in enumerate(retrieved_docs):
            chunk_text = "Document " + str(doc_num) + ":\n" + doc.content
            document_texts_list.append(chunk_text)

        document_texts = "\n\n".join(document_texts_list)

        dc_object_extraction_prompt = DC_OBJECT_NO_BASE_DATA_EXTRACTION_PROMPT.format(
            question=question,
            task=agent_1_task,
            document_text=document_texts,
            objects_of_interest=agent_1_output_objective,
        )
    else:
        dc_object_extraction_prompt = DC_OBJECT_WITH_BASE_DATA_EXTRACTION_PROMPT.format(
            question=question,
            task=agent_1_task,
            base_data=agent_1_base_data,
            objects_of_interest=agent_1_output_objective,
        )

    msg = [
        HumanMessage(
            content=dc_object_extraction_prompt,
        )
    ]
    primary_llm = graph_config.tooling.primary_llm
    # Grader
    try:
        llm_response = run_with_timeout(
            30,
            primary_llm.invoke,
            prompt=msg,
            timeout_override=30,
            max_tokens=300,
        )

        cleaned_response = (
            str(llm_response.content)
            .replace("```json\n", "")
            .replace("\n```", "")
            .replace("\n", "")
        )
        cleaned_response = cleaned_response.split("OBJECTS:")[1]
        object_list = [x.strip() for x in cleaned_response.split(";")]
    except Exception:
        pass

    write_custom_event(
        "initial_agent_answer",
        AgentAnswerPiece(
            answer_piece=" Researching the individual objects for each source type... ",
            level=0,
            level_question_num=0,
            answer_type="agent_level_answer",
        ),
        writer,
    )

    return SearchSourcesObjectsUpdate(
        analysis_objects=object_list,
        analysis_sources=document_sources,
        log_messages=["Agent 1 Task done"],
    )
