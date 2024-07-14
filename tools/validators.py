class Validator:

    def __init__(self, user_filter):
        self.user_filter = user_filter

    def validate_min_price(self, value):
        return (
            value >= self.user_filter.min_price if self.user_filter.min_price else True
        )

    def validate_max_price(self, value):
        return (
            value <= self.user_filter.max_price if self.user_filter.max_price else True
        )

    def validate_region_name(self, value):
        return (
            self.user_filter.region_name == value
            if self.user_filter.region_name and self.user_filter.region_name != "Hamısı"
            else True
        )

    def validate_make_name(self, value):
        return (
            self.user_filter.make_name == value
            if self.user_filter.make_name and self.user_filter.make_name != "Hamısı"
            else True
        )

    def validate_model_name(self, value):
        return (
            self.user_filter.model_name == value
            if self.user_filter.model_name and self.user_filter.model_name != "Hamısı"
            else True
        )
