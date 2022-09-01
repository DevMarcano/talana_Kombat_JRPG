from Kombat.models import kombat, turn
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
import json


def narrar(movimiento, player):
    descripcion = ""
    for i in movimiento:
        if i == "w":
            descripcion = descripcion + "Salta, "
        if i == "S":
            descripcion = descripcion + "Agacha, "
        if i == "A":
            if player == 1:
                descripcion = descripcion + "mueve hacia adelante, "
            else:
                descripcion = descripcion + "mueve hacia atras, "
        if i == "D":
            if player == 1:
                descripcion = descripcion + "mueve hacia atras, "
            else:
                descripcion = descripcion + "mueve hacia adelante, "
    return descripcion


def tonyturn(hpArnaldo, movimiento, golpe):
    if ((golpe == "") and (movimiento == "")):
        return [hpArnaldo, "Tonyn se salta el turno"]
    damage = 0
    realizada = 0
    descripcion = ""
    if movimiento + golpe == "":
        descripcion = "tonyn salto el turno"
    if (movimiento+golpe) == "DSDP":
        damage = 3
        descripcion = "Tonyn ha realizado Taladoken"
        realizada = 1
    if (movimiento+golpe) == "SDK":
        damage = 2
        descripcion = "Tonyn ha realizado Remuyuken"
        realizada = 1

    if realizada == 0:
        descripcion = "tonyn se " + narrar(movimiento, 1)
        if golpe == "P":
            damage = 1
            descripcion = descripcion + " y ah realizado un golpe"
        if golpe == "K":
            damage = 1
            descripcion = descripcion + " y ah realizado una patada"

    newhp = hpArnaldo - damage

    return [newhp, descripcion]


def Arnaldorturn(hpTonyn, movimiento, golpe):
    if ((golpe == "") and (movimiento == "")):
        return [hpTonyn, "Tonyn se salta el turno"]
    damage = 0
    realizada = 0
    descripcion = ""
    if movimiento + golpe == "":
        descripcion = "Arnaldor salto el turno"
    if (movimiento+golpe) == "SAK":
        damage = 3
        descripcion = "Arnaldor ha realizado Remuyuken"
        realizada = 1
    if (movimiento+golpe) == "ASAP":
        damage = 2
        descripcion = "Arnaldor ha realizado Taladoken"
        realizada = 1

    if realizada == 0:
        descripcion = "Arnaldor se " + narrar(movimiento, 2)
        if golpe == "":
            descripcion = descripcion
        if golpe == "P":
            damage = 1
            descripcion = descripcion + " y ah realizado un golpe"
        if golpe == "K":
            damage = 1
            descripcion = descripcion + " y ah realizado una patada"

    newhp = hpTonyn - damage

    return [newhp, descripcion]


@api_view(['POST'])
def narrarkombat(request):
    if json.loads(request.body):
        data = json.loads(request.body)
    else:
        return JsonResponse({"message": "error data no json formato"})

    if "player1" in data:
        if "movimientos" in data["player1"]:
            player1movement = data["player1"]["movimientos"]
        else:
            return JsonResponse({"message": "faltan movimientos de player1"})

        if "golpes" in data["player1"]:
            player1attack = data["player1"]["golpes"]
        else:
            return JsonResponse({"message": "error no golpes en player1 data"})
    else:
        return JsonResponse({"message": "error no player1 data"})

    if "player2" in data:
        if "movimientos" in data["player2"]:
            player2movement = data["player2"]["movimientos"]
        else:
            return JsonResponse({"message": "faltan movimientos de player2"})

        if "golpes" in data["player2"]:
            player2attack = data["player2"]["golpes"]
        else:
            return JsonResponse({"message": "error no golpes en player2 data"})
    else:
        return JsonResponse({"message": "error no player2 data"})
    i = 0

    if len(player1attack) != len(player1movement):
        message = "la cantidad de golpes y movimientos dispares en el player 1"
        return JsonResponse({"message": message})

    if len(player2attack) != len(player2movement):
        message = "la cantidad de golpes y movimientos dispares en el player 2"
        return JsonResponse({"message": message})

    if len(player1movement) > len(player2movement):
        numrounds = len(player1movement)
    else:
        numrounds = len(player2movement)
    round = 1
    combate = []
    hpTonyn = 6
    hpArnaldor = 6
    _winner = ""
    new_kombat = kombat.objects.create(winner=_winner)
    for i in range(numrounds):
        try:
            turnmovimiento1 = player1movement[i]
            if len(turnmovimiento1) > 5:
                new_kombat.delete()
                message = "ronda " + str(i) + " Tonyn mueve mas de 5 veces"
                return JsonResponse({"message": message})
            turngolpe1 = player1attack[i]
            if len(turngolpe1) > 1:
                new_kombat.delete()
                message = "ronda " + str(i) + " tonyn golpea mas de 1 ves"
                return JsonResponse({"message": message})
        except:
            turnmovimiento1 = ""
            turngolpe1 = ""

        try:
            turnmovimiento2 = player2movement[i]
            if len(turnmovimiento1) > 5:
                new_kombat.delete()
                message = "ronda " + str(i) + " Arnaldor mueve mas de 5 veces"
                return JsonResponse({"message": message})
            turngolpe2 = player2attack[i]
            if len(turngolpe1) > 1:
                new_kombat.delete()
                message = "ronda " + str(i) + " Arnaldor golpea mas de 1 ves"
                return JsonResponse({"message": message})
        except:
            turnmovimiento2 = ""
            turngolpe2 = ""
        # calculo de quien ira primero en la ronda de ataque
        # solo coloco los casos donde pueda ir Arnaldor de primero
        # porque de lo contrario siempre ira Tonyn primero
        total1 = len(turngolpe1)+len(turnmovimiento1)
        total2 = len(turngolpe2)+len(turnmovimiento2)
        primero = 1
        if total1 == total2:
            if len(turnmovimiento1) > len(turnmovimiento2):
                primero = 2
            else:
                if len(turngolpe1) > len(turngolpe2):
                    primero = 2
        else:
            if total1 > total2:
                primero = 2

        if primero == 1:
            jsonRound = {"round": "ronda" + str(round) + " Tonyn va primero",
                         "player1": "",
                         "player2": "",
                         "hpplayer1": "",
                         "hpplayer2": ""}
            # incio del tueno de Tonyn siendo el primero
            turnTo = tonyturn(hpArnaldor, turnmovimiento1, turngolpe1)
            if turnTo[0] < 1:
                des = " a Ganado la pelea aun tiene " + str(hpTonyn) + " hp"
                turnTo[1] = turnTo[1] + des
                jsonRound["player1"] = turnTo[1]
                jsonRound["player2"] = "Arnaldor quedo K.O."
                jsonRound["hpplayer1"] = hpTonyn
                jsonRound["hpplayer2"] = turnTo[1]
                _winner = "Tonyn"
                new_kombat.winner = _winner
                new_kombat.save()
                descripcion = jsonRound["player1"]+" "+jsonRound["player2"]
                Tonynturn = turn.objects.create(kombat_id=new_kombat,
                                                player="Tonyn",
                                                descripcion=descripcion,
                                                player1hp=hpTonyn,
                                                player2hp=hpArnaldor-turnTo[0],
                                                nround=i)
                combate.append(jsonRound)
                return(JsonResponse({"combate": combate}))
            hpArnaldor = turnTo[0]
            Tonynturn = turn.objects.create(kombat_id=new_kombat,
                                            player="Tonyn",
                                            descripcion=turnTo[1],
                                            player1hp=hpTonyn,
                                            player2hp=hpArnaldor,
                                            nround=i)
            # incio del tueno de arnaldo siendo segundo
            turnAr = Arnaldorturn(hpTonyn, turnmovimiento2, turngolpe2)
            if turnAr[0] < 1:
                des = " a Ganado la pelea aun tiene " + str(hpArnaldor) + " hp"
                turnAr[1] = turnAr[1] + des
                jsonRound["player2"] = turnAr[1]
                jsonRound["player1"] = turnTo[1] + " Tonyn quedo K.O."
                jsonRound["hpplayer1"] = turnAr[0]
                jsonRound["hpplayer2"] = hpArnaldor
                _winner = "Arnaldor"
                new_kombat.winner = _winner
                new_kombat.save()
                descripcion = jsonRound["player2"]+" "+jsonRound["player1"]
                Arnaturn = turn.objects.create(kombat_id=new_kombat,
                                               player="Arnaldor",
                                               descripcion=descripcion,
                                               player1hp=hpTonyn-turnAr[0],
                                               player2hp=hpArnaldor,
                                               nround=i)
                combate.append(jsonRound)
                return(JsonResponse({"combate": combate}))
            hpTonyn = turnAr[0]
            jsonRound["player1"] = turnTo[1]
            jsonRound["player2"] = turnAr[1]
            jsonRound["hpplayer1"] = hpTonyn
            jsonRound["hpplayer2"] = hpArnaldor
            Arnaturn = turn.objects.create(kombat_id=new_kombat,
                                           player="Arnaldor",
                                           descripcion=turnAr[1],
                                           player1hp=hpTonyn,
                                           player2hp=hpArnaldor,
                                           nround=i)
        else:
            jsonRound = {"round": str(round)+" Arnaldor va primero",
                         "player2": "",
                         "player1": "",
                         "hpplayer1": "",
                         "hpplayer2": ""}
            # inicio del tueno de Arnaldor siendo Primero
            turnAr = Arnaldorturn(hpTonyn, turnmovimiento2, turngolpe2)
            if turnAr[0] < 1:
                des = " a Ganado la pelea aun tiene " + str(hpArnaldor) + " hp"
                turnAr[1] = turnAr[1] + des
                jsonRound["player2"] = turnAr[1]
                jsonRound["player1"] = "Tonyn quedo K.O."
                jsonRound["hpplayer1"] = turnAr[0]
                jsonRound["hpplayer2"] = hpArnaldor
                _winner = "Arnaldor"
                new_kombat.winner = _winner
                new_kombat.save()
                descripcion = jsonRound["player2"]+" "+jsonRound["player1"]
                Arnaturn = turn.objects.create(kombat_id=new_kombat,
                                               player="Arnaldor",
                                               descripcion=descripcion,
                                               player1hp=hpTonyn-turnAr[0],
                                               player2hp=hpArnaldor,
                                               nround=i)
                combate.append(jsonRound)
                return(JsonResponse({"combate": combate}))
            hpTonyn = turnAr[0]
            Arnaturn = turn.objects.create(kombat_id=new_kombat,
                                           player="Arnaldor",
                                           descripcion=turnAr[1],
                                           player1hp=hpTonyn,
                                           player2hp=hpArnaldor,
                                           nround=i)
            # incio del tueno de Tonyn siendo el segundo
            turnTo = tonyturn(hpArnaldor, turnmovimiento1, turngolpe1)
            if turnTo[0] < 1:
                des = " a Ganado la pelea aun tiene " + str(hpTonyn) + " hp"
                turnTo[1] = turnTo[1] + des
                jsonRound["player1"] = turnTo[1]
                jsonRound["player2"] = turnAr[1] + " Arnaldor quedo K.O."
                jsonRound["hpplayer1"] = hpTonyn
                jsonRound["hpplayer2"] = turnTo[0]
                _winner = "Tonyn"
                new_kombat.winner = _winner
                new_kombat.save()
                descripcion = jsonRound["player1"]+" "+jsonRound["player2"]
                Tonynturn = turn.objects.create(kombat_id=new_kombat,
                                                player="Tonyn",
                                                descripcion=descripcion,
                                                player1hp=hpTonyn,
                                                player2hp=hpArnaldor-turnTo[0],
                                                nround=i)
                combate.append(jsonRound)
                return(JsonResponse({"combate": combate}))
            hpArnaldor = turnTo[0]
            jsonRound["player2"] = turnAr[1]
            jsonRound["player1"] = turnTo[1]
            jsonRound["hpplayer1"] = hpTonyn
            jsonRound["hpplayer2"] = hpArnaldor
        round = round + 1
        combate.append(jsonRound)

    return JsonResponse({"kombat": combate})
