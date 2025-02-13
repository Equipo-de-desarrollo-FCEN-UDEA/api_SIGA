from app.schemas.voting.vote import Vote


async def vote_count(votes: list[Vote]) -> int:
    positive_votes = votes.count('POSITIVO')
    negative_votes = votes.count('NEGATIVO')

    return positive_votes, negative_votes

