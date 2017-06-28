# coding: utf-8


class Response(object):
    ReasonPayloadEmpty = "PayloadEmpty"
    # The message payload was too large. The maximum payload size is 4096 bytes.
    ReasonPayloadTooLarge = "PayloadTooLarge"
    # The apns-topic was invalid.
    ReasonBadTopic = "BadTopic"
    # Pushing to this topic is not allowed.
    ReasonTopicDisallowed = "TopicDisallowed"
    # The apns-id value is bad.
    ReasonBadMessageID = "BadMessageId"
    # The apns-expiration value is bad.
    ReasonBadExpirationDate = "BadExpirationDate"
    # The apns-priority value is bad.
    ReasonBadPriority = "BadPriority"
    # The device token is not specified in the request :path. Verify that the
    # :path header contains the device token.
    ReasonMissingDeviceToken = "MissingDeviceToken"
    # The specified device token was bad. Verify that the request contains a valid
    # token and that the token matches the environment.
    ReasonBadDeviceToken = "BadDeviceToken"
    # The device token does not match the specified topic.
    ReasonDeviceTokenNotForTopic = "DeviceTokenNotForTopic"
    # The device token is inactive for the specified topic.
    ReasonUnregistered = "Unregistered"
    # One or more headers were repeated.
    ReasonDuplicateHeaders = "DuplicateHeaders"
    # The client certificate was for the wrong environment.
    ReasonBadCertificateEnvironment = "BadCertificateEnvironment"
    # The certificate was bad.
    ReasonBadCertificate = "BadCertificate"
    # The specified action is not allowed.
    ReasonForbidden = "Forbidden"
    # The request contained a bad :path value.
    ReasonBadPath = "BadPath"
    # The specified :method was not POST.
    ReasonMethodNotAllowed = "MethodNotAllowed"
    # Too many requests were made consecutively to the same device token.
    ReasonTooManyRequests = "TooManyRequests"
    # Idle time out.
    ReasonIdleTimeout = "IdleTimeout"
    # The server is shutting down.
    ReasonShutdown = "Shutdown"
    # An internal server error occurred.
    ReasonInternalServerError = "InternalServerError"
    # The service is unavailable.
    ReasonServiceUnavailable = "ServiceUnavailable"
    # The apns-topic header of the request was not specified and was required.
    # The apns-topic header is mandatory when the client is connected using a
    # certificate that supports multiple topics.
    ReasonMissingTopic = "MissingTopic"

    def __init__(
        self, status_code: int, apns_id: str,
        timestamp=None, reason=None,
    ):

        # The HTTP status code retuened by APNs.
        # A 200 value indicates that the notification was successfully sent.
        # For a list of other possible status codes, see table 6-4 in the Apple Local
        # and Remote Notification Programming Guide.
        self.status_code = status_code

        # The APNs error string indicating the reason for the notification failure (if
        # any). The error code is specified as a string. For a list of possible
        # values, see the Reason constants above.
        # If the notification was accepted, this value will be "".
        self.reason = reason

        # The APNs ApnsID value from the Notification. If you didn't set an ApnsID on the
        # Notification, this will be a new unique UUID which has been created by APNs.
        self.apns_id = apns_id

        # If the value of StatusCode is 410, this is the last time at which APNs
        # confirmed that the device token was no longer valid for the topic.
        self.timestamp = timestamp
