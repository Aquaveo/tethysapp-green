from tethysext.atcore.models.app_users import Resource


class GsshaModel(Resource):
    TYPE = 'gssha-model-resource'
    DISPLAY_TYPE_SINGULAR = 'GSSHA Model'
    DISPLAY_TYPE_PLURAL = 'GSSHA Models'

    # Polymorphism
    __mapper_args__ = {
        'polymorphic_identity': TYPE,
    }
