class DesignWork(object):
    def __init__(self, work_type: int, production_id: str, charming: int = None, designer_company_id: str = None,
                 production_t_plus: int = None):
        self.work_type = work_type
        self.production_id = production_id
        self.charming = charming
        self.designer_company_id = designer_company_id
        self.production_t_plus = production_t_plus
