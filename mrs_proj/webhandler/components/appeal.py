from django_unicorn.components import UnicornView
from webhandler.models import SupportTicket


class AppealView(UnicornView):
    email = ""
    message = ""
    open_tickets = []

    def mount(self):
        self.load_open_tickets()

    def load_open_tickets(self):
        self.open_tickets = SupportTicket.objects.filter(user=self.request.user, status="open")

    def add_comment(self):
        if self.email and self.message:
            SupportTicket.objects.create(
                user=self.request.user,
                email=self.email,
                message=self.message,
                status="open",
            )
            self.email = ""
            self.message = ""
            self.load_open_tickets()  # Reload open tickets after adding a comment
            self.call("alert", "Комментарий добавлен успешно!")
        else:
            self.call("alert", "Заполните все поля!")

    class Meta:
        model = SupportTicket
        fields = ['email', 'message']
