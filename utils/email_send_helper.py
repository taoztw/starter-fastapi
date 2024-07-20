# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
from config import settings

from alibabacloud_dm20151123.client import Client as Dm20151123Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dm20151123 import models as dm_20151123_models
from alibabacloud_tea_util import models as util_models
from exts import logger
import traceback


class EmailHelper:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Dm20151123Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=settings.ALIBABA_CLOUD_ACCESS_KEY_ID,
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=settings.ALIBABA_CLOUD_ACCESS_KEY_SECRET,
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Dm
        config.endpoint = f"dm.aliyuncs.com"
        return Dm20151123Client(config)

    @staticmethod
    def main(
        to_address: str,
        subject: str,
        html_body: str,
    ) -> None:
        client = EmailHelper.create_client()
        single_send_mail_request = dm_20151123_models.SingleSendMailRequest(
            account_name=settings.EMAIL_SENDER,
            address_type=1,
            reply_to_address=False,
            to_address=to_address,
            subject=subject,
            html_body=html_body,
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.single_send_mail_with_options(single_send_mail_request, runtime)
        except Exception as error:
            logger.error(
                f"邮箱发送失败: {error}, {error.message}\n 详细错误情况: {traceback.format_exc()}\n诊断地址 {error.data.get('Recommend')}"
            )

    @staticmethod
    async def main_async(
        to_address: str,
        subject: str,
        html_body: str,
    ) -> None:
        client = EmailHelper.create_client()
        single_send_mail_request = dm_20151123_models.SingleSendMailRequest(
            account_name=settings.EMAIL_SENDER,
            address_type=1,
            reply_to_address=False,
            to_address=to_address,
            subject=subject,
            html_body=html_body,
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.single_send_mail_with_options_async(
                single_send_mail_request, runtime
            )
        except Exception as error:
            logger.error(
                f"邮箱发送失败: {error}, {error.message}\n 详细错误情况: {traceback.format_exc()}\n诊断地址 {error.data.get('Recommend')}"
            )


if __name__ == "__main__":
    from asserts.template.email_tempalte.email_tempalte import verify_email

    html_body = verify_email.format(code="12313")

    EmailHelper.main(
        to_address="", html_body=html_body, subject="邮箱验证"
    )
