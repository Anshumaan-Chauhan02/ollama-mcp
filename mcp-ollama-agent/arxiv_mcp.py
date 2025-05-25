"""
Do not name the file arxiv.py, as then it interferes with the package arxiv.
You will recieve "AttributeError: partially initialized module 'arxiv'" error
"""
from mcp.server.fastmcp import FastMCP
import arxiv

mcp = FastMCP("arxiv")

@mcp.tool()
async def arxiv_papers(topic: str) -> dict[str, str] | None:
    """
    Fetch summaries and titles of the 20 most recently submitted papers from arXiv related to a given topic.

    This function queries the arXiv API using the provided topic string and retrieves the 20 latest papers,
    sorted by submission date in descending order (most recent first). It returns a dictionary where each key 
    is the paper's title and each corresponding value is the paper's abstract (summary).

    Parameters:
        topic (str): The search topic or keyword to query relevant papers on arXiv.

    Returns:
        dict[str, str] | None: A dictionary mapping paper titles to their summaries, or None if no results are found.
    """
    # Default API Client
    client = arxiv.Client()

    # Top 10 relevent papers
    # Sort by  - Relevance, LastUpdatedDate, LastUpdatedDate
    # Sorting order - Ascending, Descending
    search = arxiv.Search(
        query = topic,
        max_results = 20,
        sort_by = arxiv.SortCriterion.SubmittedDate,
        sort_order = arxiv.SortOrder.Descending
        )

    results = client.results(search)
    relevant_details = {}
    for r in results:
        # For more details on the attributes available for the Result class:
        # https://github.com/lukasschwab/arxiv.py/blob/master/arxiv/__init__.py#L28
        relevant_details[r.title] = r.summary
    return relevant_details
    

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')



