import pytest

from scripts.slack_notification import (
    parse_environment_variables,
    post_slack_notification,
)


def test_parse_environment_variables(monkeypatch):
    monkeypatch.setenv("SLACK_AUTH_TOKEN", "token")
    monkeypatch.setenv("SLACK_CHANNEL_NAME", "test-alerts")
    monkeypatch.setenv("CONTENT", "Slack message")

    slack_environment_variables = parse_environment_variables()

    assert slack_environment_variables == {
        "attachment_filename": None,
        "content": "Slack message",
        "file_type": "yaml",
        "initial_comment": "",
        "slack_auth_token": "token",
        "slack_channel": "test-alerts",
        "title": "",
    }


def test_parse_environment_variables_missing_slack_token(monkeypatch):
    monkeypatch.setenv("SLACK_CHANNEL_NAME", "test-alerts")
    monkeypatch.setenv("CONTENT", "Slack message")

    with pytest.raises(SystemExit):
        parse_environment_variables()


def test_parse_environment_variables_missing_slack_channel_name(monkeypatch):
    monkeypatch.setenv("SLACK_AUTH_TOKEN", "token")
    monkeypatch.setenv("CONTENT", "Slack message")

    with pytest.raises(SystemExit):
        parse_environment_variables()


def test_parse_environment_variables_content_and_attachment_filename_set(monkeypatch):
    monkeypatch.setenv("SLACK_AUTH_TOKEN", "token")
    monkeypatch.setenv("SLACK_CHANNEL_NAME", "test-alerts")
    monkeypatch.setenv("CONTENT", "Slack message")
    monkeypatch.setenv("ATTACHMENT_FILENAME", "file_name")

    with pytest.raises(SystemExit):
        parse_environment_variables()


def test_parse_environment_variables_no_content_or_attachment_filename_set(monkeypatch):
    monkeypatch.setenv("SLACK_AUTH_TOKEN", "token")
    monkeypatch.setenv("SLACK_CHANNEL_NAME", "test-alerts")

    with pytest.raises(SystemExit):
        parse_environment_variables()


def test_parse_environment_variables_attachment_filename_not_valid(monkeypatch):
    monkeypatch.setenv("SLACK_AUTH_TOKEN", "token")
    monkeypatch.setenv("SLACK_CHANNEL_NAME", "test-alerts")
    monkeypatch.setenv("ATTACHMENT_FILENAME", "file_name")

    with pytest.raises(SystemExit):
        parse_environment_variables()


def test_post_slack_notification_with_ok_response_raises_no_error(mocker):
    mocker.patch("slack.web.client.WebClient.files_upload", return_value={"ok": True})

    post_slack_notification(
        slack_auth_token="token",
        slack_channel="test-alerts",
        content="slack message",
        file_type="type",
        title="title",
        initial_comment="comment",
        attachment_filename="file",
    )


def test_post_slack_notification_with_no_content_and_ok_response_raises_no_error(
    mocker,
):
    mocker.patch("slack.web.client.WebClient.files_upload", return_value={"ok": True})
    post_slack_notification(
        slack_auth_token="token",
        slack_channel="test-alerts",
        file_type="type",
        title="title",
        content=None,
        initial_comment="comment",
        attachment_filename="file",
    )


def test_post_slack_notification_with_bad_response_raises_error(mocker):
    mocker.patch("slack.web.client.WebClient.files_upload", return_value={"ok": False})

    with pytest.raises(SystemExit):
        post_slack_notification(
            slack_auth_token="token",
            slack_channel="test-alerts",
            content="slack message",
            file_type="type",
            title="title",
            initial_comment="comment",
            attachment_filename="file",
        )


def test_post_slack_notification_with_api_error_exits():

    with pytest.raises(SystemExit):
        post_slack_notification(
            slack_auth_token="token",
            slack_channel="test-alerts",
            content="slack message",
            file_type="type",
            title="title",
            initial_comment="comment",
            attachment_filename="file",
        )
