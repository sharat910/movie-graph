from pydantic import BaseModel

# Define Pydantic models

class Character(BaseModel):
    """
    Represents an individual in the movie plot.

    This model captures basic information about a character in the movie, including their name,
    a brief summary of their role in the plot.
    """
    name: str
    role: str

class Relationship(BaseModel):
    """
    Represents the relationship summary between two people in the movie plot.
    For example, if character1 and character2 are friends, then relationship_summary is friends. 
    If they briefly interacted and character1 hit character2, then relationship_summary is "assaulted in a fight (or any other relevant context)" etc.
    It is directional, so if character1 is father of character2, then relationship_summary is "father of" (not son of).
    """
    character1_name: str
    character2_name: str
    relationship_summary: str

class PlotResponse(BaseModel):
    """
    Represents the structured response for a movie plot analysis.

    This model aggregates information about characters, relationships, along with a summary of the plot given.

    It maintains accurate and consistent names between character and relationship models.
    """
    characters: list[Character]
    relations: list[Relationship]
    summary: str