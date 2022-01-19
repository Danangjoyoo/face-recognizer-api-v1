from ...dependencies.log import logger
from ...dependencies.utils import create_response, create_status, BaseCRUD, status
from ...database import models

crud = BaseCRUD(models.Client)