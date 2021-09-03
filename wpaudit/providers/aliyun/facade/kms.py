from aliyunsdkkms.request.v20160120 import ListKeysRequest, DescribeKeyRequest

from wpaudit.core.console import print_exception
from wpaudit.providers.aliyun.authentication_strategy import AliyunCredentials
from wpaudit.providers.aliyun.facade.utils import get_response
from wpaudit.providers.aliyun.utils import get_client


class KMSFacade:
    def __init__(self, credentials: AliyunCredentials):
        self._credentials = credentials

    async def get_keys(self, region):
        """
        Get all keys

        :return: a list of all keys
        """
        try:
            client = get_client(credentials=self._credentials, region=region)
            response = await get_response(client=client,
                                          request=ListKeysRequest.ListKeysRequest())
            if response:
                return response['Keys']['Key']
            else:
                return []
        except Exception as e:
            print_exception(f'Failed to get KMS keys: {e}')
            return []

    async def get_key_details(self, key_id, region):
        """
        Gets details for a key

        :return: a dictionary of details
        """
        try:
            client = get_client(credentials=self._credentials, region=region)
            request = DescribeKeyRequest.DescribeKeyRequest()
            request.set_KeyId(key_id)
            response = await get_response(client=client,
                                          request=request)
            if response:
                return response['KeyMetadata']
            else:
                return []
        except Exception as e:
            print_exception(f'Failed to get KMS key details: {e}')
            return []
