import os
import tempfile
import zipfile
from tethysext.atcore.exceptions import ModelDatabaseInitializationError, ATCoreException
from tethysext.atcore.controllers.app_users import ModifyResource
from tethysext.atcore.services.model_database import ModelDatabase
from gsshapyorm.orm import DeclarativeBase as GsshaPyBase, ProjectFile
from tethysapp.green.app import Green as app


class ModifyGsshaModel(ModifyResource):
    include_srid = True
    srid_required = True
    include_file_upload = True
    file_upload_required = True
    file_upload_accept = "zip"
    file_upload_label = "GSSHA Model Zip File"
    file_upload_help = "Upload a zip archive containing the files for a GSSHA model."
    file_upload_error = "Must provide GSSHA file(s)."

    def handle_resource_finished_processing(self, session, request, request_app_user, resource, editing):
        """
        Hook to allow for post processing after the resource has finished being created or updated.
        Args:
            session(sqlalchemy.session): open sqlalchemy session.
            request(django.request): the Django request.
            request_app_user(AppUser): app user that is making the request.
            resource(Resource): The resource being edited or newly created.
            editing(bool): True if editing, False if creating a new resource.
        """
        if not editing:
            # put resource creation logic here
            # load files into database
            # create geoserver layers
            # Create a new model database
            model_db = ModelDatabase(app=app)
            model_db_success = model_db.initialize(declarative_bases=(GsshaPyBase,), spatial=True)

            # Initialize GsshaPy Tables on Model database
            if not model_db_success:
                raise ModelDatabaseInitializationError('An error occurred while trying to initialize a model database.')

            # Set custom attributes
            resource.set_attribute('database_id', model_db.get_id())

            # Parse zip
            zip_path = resource.get_attribute('files')[0]
            with tempfile.TemporaryDirectory() as temp_dir, \
                 zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

                # find the .prj file
                prj_file = None
                prj_dir = None

                for (root, _, files) in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.prj'):
                            prj_file = os.path.join(root, file)
                            prj_dir = root
                            break

                if not prj_dir or not prj_file:
                    raise ATCoreException('No .prj file found in given zip archive.')
    
                model_db_session = model_db.get_session()
                
                try:
                    project_file = ProjectFile()
                    
                    srid = int(resource.get_attribute('srid'))
                    project_file.readProject(
                        directory=prj_dir,
                        projectFileName=prj_file,
                        session=model_db_session,
                        spatial=True,
                        spatialReferenceID=srid
                    )
                finally:
                    model_db_session.close()
