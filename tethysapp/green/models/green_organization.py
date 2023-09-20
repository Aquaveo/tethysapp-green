from tethysext.atcore.models.app_users import Organization


class GreenOrganization(Organization):
    TYPE = 'green-organization'

    # Polymorphism
    __mapper_args__ = {
        'polymorphic_identity': TYPE,
    }
