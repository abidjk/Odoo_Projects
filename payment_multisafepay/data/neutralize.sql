-- disable multisafepay payment provider
UPDATE payment_provider
   SET multisafepay_api_key = NULL;