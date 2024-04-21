#Proof of Concept for a Notification System

from plyer import notification # pip install plyer


notification.notify(
    title = 'testing',
    message = 'message',
    app_icon = None,
    timeout = 10,
)