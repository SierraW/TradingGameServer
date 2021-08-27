from models.GameData import GameData
from models.cities.personality.PersonalityOffer import PersonalityOffer
from models.cities.personality.PersonalityWorkContract import PersonalityWorkContract


def work_contract_accept_offer(game_data: GameData, offer: PersonalityOffer, human_id: str):
    start_t = game_data.environment.time.copy()
    end_t = start_t.offset(month=offer.duration_months)
    # TODO one_time payment
    work_contract = PersonalityWorkContract(start_t=start_t, end_t=end_t, worker_id=human_id,
                                            receiver_company_id=offer.company_id,
                                            receiver_property_id=offer.property_id,
                                            work_days=offer.work_days,
                                            one_time_payment=offer.one_time_payment,
                                            salary_monthly=offer.monthly_salary)
    contract_id = game_data.generate_identifier()
    game_data.work_contracts[contract_id] = work_contract
    prop = game_data.properties[offer.property_id]
    prop.work_contract_id_list.append(contract_id)
    human = game_data.humans[human_id]
    human.personality_work_contracts.append(contract_id)
