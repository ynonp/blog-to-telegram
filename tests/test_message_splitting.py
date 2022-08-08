import blog_to_telegram.publish_daily_post as app

def test_split_message():
    msg = """
this is a long message
that should be split into multiple
messages
"""
    parts = app.split_body_to_messages(msg, 80)
    assert [
            "this is a long message\nthat should be split into multiple\n",
            "messages\n"
            ] == parts


def test_code_blocks_are_split():
    msg = """
this is a long message
that includes a code block

```
import sys

print("one")
print("two")
print("three")
print("four")
```
"""
    parts = app.split_body_to_messages(msg, 50)
    assert [
            "this is a long message\n",
            'that includes a code block\n',
            '```\nimport sys\n\nprint("one")\n```\n',
            '```\nprint("two")\nprint("three")\n```\n',
            '```\nprint("four")\n```\n'
            ] == parts



