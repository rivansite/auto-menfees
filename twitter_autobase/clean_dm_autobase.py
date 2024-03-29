import re


def clean_private_autobase(selfAlias: object, message: str, media_idsAndTypes: list, list_attchmentUrlsMedia: list) -> str:
    '''
    Move url from list_attachmentUrlsMedia to media_idsAndTypes
    :param media_idsAndTypes: list of media ids and media types that returned from upload_media_tweet method
    :param list_attachmentUrlsMedia: list of (url on dm, extended url)
    :return: message
    '''
    for media_tweet_url in list_attchmentUrlsMedia:
        list_mediaIdsAndTypes = selfAlias.upload_media_tweet(media_tweet_url[1])
        if len(list_mediaIdsAndTypes):
            media_idsAndTypes.extend(list_mediaIdsAndTypes)
            message = message.split(" ")
            message.remove(media_tweet_url[0])
            message = " ".join(message)
    
    return message


def clean_main_autobase(selfAlias: object, message: str, attachment_urls: tuple) -> str:
    '''
    Clean dm based on config.py
    :param attachment_urls: (url on dm, extended url)
    :return: message
    '''
    # Keyword Deleter
    if selfAlias.credential.Keyword_deleter:
        list_keyword = [j.lower() for j in selfAlias.credential.Trigger_word]
        
        for word in list_keyword:
            tmp_message = message.lower()
            pos = tmp_message.find(word)
            
            if pos != -1:
                replaced = message[pos : pos + len(word)]
                
                if pos == 0:
                    if len(word) == len(message):
                        pass
                        # Error will happen on post_tweet method. If the message only contains trigger
                        # that will be deleted on replaced variable
                    elif message[pos+len(word)] == " ":
                        # when trigger is placed on the start of text and there is a space after it
                        replaced += " "

                elif message[pos-1] == " ":
                    # when trigger is placed on the middle or the end of text
                    replaced = " " + replaced
                
                message = message.replace(replaced, "")

    # Cleaning attachment_url
    if attachment_urls != (None, None):
        message = message.split(" ")
        if attachment_urls[0] in message:
            message.remove(attachment_urls[0])
        message = " ".join(message)
                            
    # Cleaning hashtags and mentions
    message = message.replace("#", "#.")
    message = message.replace("@", "@.")

    return message


def count_emoji(text: str) -> int:
    '''
    Count emojis on the text
    '''
    # Ref: https://gist.github.com/Alex-Just/e86110836f3f93fe7932290526529cd1#gistcomment-3208085
    # Ref: https://en.wikipedia.org/wiki/Unicode_block
    emoji = re.compile("["
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251" 
        "]+")
    
    return len(re.findall(emoji, text))


def search_list_media_ids(media_idsAndTypes: list) -> list:
    '''
    Manage and divide media ids from media_idsAndTypes
    :return: list of list media_ids per 4 photo or 1 video/gif e.g. [[media_ids],[media_ids],[media_ids]]
    '''
    list_media_ids = [[]] # e.g. [[media_ids],[media_ids],[media_ids]]
    temp = 0
    
    while len(media_idsAndTypes):
        if temp == 0:
            temp = 1
            list_media_ids = list()
        media_ids = list()
        added = 0
        for media_id, media_type in media_idsAndTypes[:4]:
            if media_type == 'video' or media_type == 'animated_gif':
                if added == 0:
                    media_ids.append(media_id)
                    added += 1
                break
            media_ids.append(media_id)
            added += 1

        list_media_ids.append(media_ids)
        # media_idsAndTypes are dynamic here
        media_idsAndTypes = media_idsAndTypes[added:]
    
    return list_media_ids