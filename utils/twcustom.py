
from twilio.twiml.voice_response import VoiceResponse


class CustomVoiceResponse(VoiceResponse):
    voice = "Polly.Arthur-Neural"

    # gather parameters
    timeout = 3
    language = "en-GB"
    speech_model = "phone_call"  # phone_call | experimental_conversations | default
    enhanced = "true"  # true | false

    def say(self, message=None, voice=None, loop=None, language=None, **kwargs):
        super().say(message, voice=self.voice, language=self.language)

    def gather(
        self,
        input=None,
        action=None,
        method=None,
        timeout=None,
        speech_timeout=None,
        max_speech_time=None,
        profanity_filter=None,
        finish_on_key=None,
        num_digits=None,
        partial_result_callback=None,
        partial_result_callback_method=None,
        language=None,
        hints=None,
        barge_in=None,
        debug=None,
        action_on_empty_result=None,
        speech_model=None,
        enhanced=None,
        **kwargs
    ):
        super().gather(
            input="speech",
            action=action,
            method="POST",
            timeout=timeout,
            speech_timeout=self.timeout,
            max_speech_time=120,
            profanity_filter=profanity_filter,
            finish_on_key=finish_on_key,
            num_digits=num_digits,
            partial_result_callback=partial_result_callback,
            partial_result_callback_method="POST",
            language=self.language,
            hints=hints,
            barge_in=barge_in,
            debug=debug,
            action_on_empty_result=None,
            speech_model=self.speech_model,
            enhanced=self.enhanced,
            **kwargs
        )
        super().redirect(url=action_on_empty_result, method="POST")

