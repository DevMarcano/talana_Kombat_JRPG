from django.db import models


class kombat(models.Model):
    winner = models.CharField(max_length=250, blank=True, null=False)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def Serialize(self):
        return {"id": self.pk,
                "Winner": self.winner,
                "date": self.date}


class turn(models.Model):
    kombat_id = models.ForeignKey(kombat, on_delete=models.CASCADE)
    player = models.CharField(max_length=250, blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=False, null=False,
                                   default="Paso el turno")
    player1hp = models.IntegerField(blank=False, null=False)
    player2hp = models.IntegerField(blank=False, null=False)
    nround = models.IntegerField(blank=False, null=False, default=0)

    def Serialize(self):
        return {"roud": self.nround,
                "Player": self.player,
                "descripcion": self.descripcion,
                "player1hp": self.player1hp,
                "player2hp": self.player2hp}
