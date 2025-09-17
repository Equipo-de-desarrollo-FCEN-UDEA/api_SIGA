from __future__ import annotations

from app.infraestructure.db.models.voting.voting import Voting
from app.infraestructure.policies.application.type.commission import CommissionFlow
from app.infraestructure.policies.application.type.mobility import MobilityFlow
from app.infraestructure.policies.application.type.purchase import PurchaseFlow
from app.infraestructure.policies.voting.vote import vote_count
from app.protocols.db.models.voting.voting_info import VotingResult
from app.schemas.voting.vote import Vote
from app.schemas.voting.voting import VotingResponse
from app.services.application.type.mobility import mobility_svc
from app.services.voting.voting_info import voting_info_svc


async def get_application_in_mongo(
    *,
    voting,
    db,
) -> dict:
    voting_id = voting.id
    user_application_id = voting.user_application_id
    application_type = voting.user_application.application.name

    voting = VotingResponse.model_validate(voting)
    voting = VotingResponse.model_dump(voting)

    if application_type == 'MOVILIDAD':
        mobility = {
            'mobility': await mobility_svc.get(id=user_application_id, db=db),
        }
        info_voting = {
            'info_voting': await voting_info_svc.get(id=voting_id, db=db),
        }
        voting['user_application'].update(mobility)
        voting.update(info_voting)
        return voting
    return {}


async def voting_result(votes: list[Vote]) -> VotingResult:
    votes = [vote.vote_type.name for vote in votes]
    if 'CONSENSO' in votes:
        return VotingResult.MEETING
    positive_votes, negative_votes = await vote_count(votes)
    if positive_votes > negative_votes:
        return VotingResult.APPROVED
    elif positive_votes < negative_votes:
        return VotingResult.REJECTED
    else:
        return VotingResult.MEETING


async def update_application_status(
        *,
        voting: Voting,
        db_postgres,
        current_user,
        result,
):
    user_application = voting.user_application

    if user_application.application.name == 'MOVILIDAD':
        application_flow = MobilityFlow(user_application)
    elif user_application.application.name == 'COMISION':
        application_flow = CommissionFlow(user_application)
    elif user_application.application.name == 'COMPRA':
        application_flow = PurchaseFlow(user_application)

    await application_flow.next(
        is_approved=result == VotingResult.APPROVED,
        db_postgres=db_postgres,
        current_user=current_user,
    )
