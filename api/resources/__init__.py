from flask_restful import Api

from main import main as main_blueprint
from bucketlist import BucketList

api = Api('rc_bucketlist', __name__, url_prefix='api/v1')
