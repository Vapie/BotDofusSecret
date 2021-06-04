import requests
import json
from enum import Enum
from typing import Any, List, TypeVar, Callable

#TODO mettre dans un ficher tools_Scripts dans classes
from classes.coord import Coord


def from_list(f: Callable[[Any], TypeVar("T")], x: Any) -> List[TypeVar("T")]:
    assert isinstance(x, list)
    return [f(y) for y in x]

#TODO mettre dans un ficher dans classe
class Direction(Enum):
    RIGHT = "right"
    LEFT = "left"
    UP = "up"
    DOWN = "down"

class Hint:
    n: int
    coord: Coord
    d: int
    label: str

    def __init__(self, n: int, x: int, y: int, d: int) -> None:

        self.n = n
        self.coord = Coord(x,y)
        self.d = d
        self.label = Hint.from_id_hint_text(n)

    @staticmethod
    def from_dict(obj: Any) -> 'Hint':
        assert isinstance(obj, dict)
        n = int(obj.get("n"))
        x = int(obj.get("x"))
        y = int(obj.get("y"))
        d = int(obj.get("d"))
        return Hint(n, x, y, d)

    def from_id_hint_text(id: int) -> str:
        return {100: 'Citrouille', 101: 'Brouette de citrouilles', 102: 'Râteau', 103: 'Fourche',
                104: 'Silo vide', 105: 'Caisse', 106: 'Caisse explosive', 107: 'Poubelle', 108: 'Ancre',
                109: 'Etendoir à linge', 110: 'Banc', 111: 'Seau plein', 112: 'Seau vide', 113: 'Roseaux',
                114: 'Chariot de mineur', 115: 'Charrette', 116: 'Chariot', 117: 'Chariot de Cawottes',
                118: 'Rondelles de Cawottes', 120: 'Puits', 121: 'Bijoux de famille', 122: 'Objet de désir',
                123: 'Bûche phallique', 124: 'Drapeau Wabbit', 125: 'Chaise de plage', 130: 'Epouvantail',
                131: 'Epouvantail', 132: 'Hache', 133: 'Pont en pierre', 135: 'Boîte aux lettres',
                136: 'Echelle', 138: 'Ossements', 139: 'Crâne de Dragon', 140: 'Arc', 141: 'Flèche',
                142: 'Botte', 143: 'Panneau avec tête de mort', 145: 'Totem', 146: 'Transporteur',
                147: 'Corbac', 148: 'Oiseau noir', 150: 'Volatile sombre', 151: 'Statue Koalak',
                152: 'Statue de classe', 155: 'Statue cyclope', 156: 'Tombe', 157: 'Tombe Koalak',
                158: 'Statue Dragodinde', 159: 'Statue Dragodinde éteinte',
                160: 'Statue Dragodinde allumée', 161: 'Statue Dragodinde sans socle',
                162: 'Feuilles de papier', 163: 'Oiseau aux yeux globuleux',
                164: 'Volatile aux yeux globuleux', 166: 'Bouclier', 168: 'Bouclier de Pandala',
                169: 'Bouclier cochon', 170: 'Bouclier Iop', 171: 'Bouclier Wabbit',
                172: 'Bouclier croissant de lune', 173: 'Bouclier en peau noire et blanche',
                174: 'Bouclier barré', 175: 'Bouclier étoilé', 176: 'Bouclier à anneaux',
                177: 'Bouclier à cornes', 178: 'Bouclier à pointes', 179: 'Bouclier gelé',
                180: 'Epouvantail Minotoror', 181: 'Paille', 182: 'Stèle', 183: 'Stèle en bois',
                184: 'Stèle en pierre', 185: 'Panneau de pêcheur', 186: 'Caisse de pain',
                187: 'Sac rapiécé', 188: 'Masse enfoncée dans le sol', 189: 'Trident planté',
                195: "Bernard-l'ermite", 196: 'Charrette de laine de Bouftou', 197: 'Charrette mordillée',
                198: 'Charrette géante en bois', 199: 'Charrette géante en bois vide',
                200: 'Charrette géante en bois pleine', 201: 'Attelage de Bouftous', 202: 'Roue en bois',
                203: 'Entrée de mine en bois', 204: 'Objet flottant', 205: 'Bouteille flottante',
                206: 'Tofu flottant', 207: 'Chapeau flottant', 208: 'Sac flottant', 209: 'Seau flottant',
                210: 'Sac flottant', 211: 'Sac flottant', 212: 'Volatile flottant', 214: 'Balai',
                215: 'Puits couvert', 216: 'Puits tâché', 217: 'Puits non couvert', 218: 'Cadavre calciné',
                219: 'Dépouille brûlée', 220: 'Totem de Moon couché', 221: 'Papillon',
                222: 'Rocher Bouftou', 223: "Squelette d'humanoïde assis",
                224: "Squelette d'humanoïde poignardé", 225: "Squelette d'humanoïde allongé",
                226: "Squelette d'humanoïde suppliant", 227: 'Squelette de Dragodinde',
                228: "Squelette d'humanoïde", 229: 'Colonne vertébrale imposante',
                230: 'Squelette de Dragon', 231: 'Patte de Dragon', 232: 'Aile de Dragon squelettique',
                234: 'Porte avec quatre troncs', 235: 'Fontaine', 236: 'Planche de glisse', 237: 'Rafiot',
                238: 'Chaloupe', 239: 'Chaudière', 240: 'Caisse de fruits rouges',
                241: 'Totem Kanniboul joyeux', 242: 'Totem Kanniboul triste',
                243: 'Totem Kanniboul colérique', 244: 'Totem Kanniboul cornu', 245: 'Roulotte',
                246: 'Bouée', 247: 'Catapulte', 248: 'Séchoir à viande', 249: 'Brochette de Tofu',
                250: 'Tour de guet', 251: 'Cible', 252: 'Scaphandre', 253: 'Robinet', 254: 'Lanterne',
                255: 'Astrolabe sphérique', 257: 'Coffre', 258: 'Totem Bouftou en bois', 259: 'Phare',
                26: 'Statue Ecaflip', 260: "Panneau d'enclos", 261: 'Tofu mort', 262: 'Cage',
                263: 'Statue Pandawa guérisseur', 264: 'Statue Pandawa en chocolat', 265: 'Paquet Pandawa',
                266: 'Piquet en bois', 267: 'Distributeur de liqueur', 27: 'Phénix', 270: 'Crustacé',
                271: 'Coquillage et sa perle', 272: 'Anémone', 273: 'Grande plaque verticale en pierre',
                274: 'Tonneau', 275: 'Jarre', 276: 'Champignon', 277: 'Pilier en pierre',
                278: 'Squelette de Boufmouth', 279: 'Canon', 28: 'Statue Crâ', 280: 'Statue Lenald',
                281: 'Statue Lenald décapitée', 282: 'Tente', 283: 'Tente de Sanglier',
                284: 'Tente cornue de Sanglier', 285: 'Tente de Mulou', 286: 'Tente cornue de Mulou',
                287: 'Boîte à outils', 288: 'Tente en cours de construction', 29: 'Statue Eniripsa',
                290: "Pot d'huile", 291: 'Boîte à outils', 292: 'Bottes suspendues', 293: 'Traineau',
                294: 'Traineau piloté par un Mansot', 295: 'Traineau détruit',
                296: 'Traîneau rempli de bois', 297: "Traineau recouvert d'une couverture",
                298: 'Traineau avec un coussin', 299: 'Panneau avec 3 directions', 30: 'Statue Enutrof',
                300: 'Panneau "Chute de pierres"', 301: 'Tapis en peau de monstre', 302: 'Trio de tonneaux',
                303: 'Planches contre deux caisses', 304: 'Caisses empilées cachées par des planches',
                305: 'Sapin en filet', 306: 'Créature gelée', 307: 'Kaniglou gelé', 308: 'Mansot gelé',
                309: 'Mansot et son poisson gelés', 31: 'Statue Féca', 310: 'Kaniglou et sa cawotte gelés',
                311: 'Mansot et son poisson et sa cawotte gelés', 312: 'Mansot et sa cawotte gelés',
                313: 'Kaniglou et sa coiffe de glace', 314: 'Mansot et sa coiffe de glace',
                315: 'Manomètre', 317: 'Caisse de pêcheur', 318: 'Tonneau de poisson',
                319: 'Filet de fruits', 32: 'Statue Iop', 320: 'Tas de planches avec une hache',
                321: 'Pelle', 322: 'Poisson qui cuit', 323: 'Tonneau couché',
                324: 'Tonneau couché avec robinet', 325: 'Coffre cadenassé',
                326: 'Coffres cadenassés superposés', 328: 'Grue', 329: 'Fagots de branches',
                33: 'Statue Osamodas', 330: 'Rondin de bois', 331: 'Tube ouvert', 332: "Tube d'alchimiste",
                334: 'Tube fermé', 335: 'Charrette avec un ballot de paille', 336: 'Barre de métal courbée',
                337: 'Statue décapitée', 338: 'Cloche', 34: 'Statue Sadida', 340: 'Croix tombale',
                342: 'Fumerolle', 343: 'Fumerolle bouchée', 344: 'Fumerolle à bulles', 345: 'Source chaude',
                346: 'Machine à vapeur', 347: 'Tripode à vapeur', 348: 'Panneau "Volcan"',
                349: 'Caisse prise dans la neige', 35: 'Statue Sram', 350: 'Engrenage', 351: 'Lampadaire',
                352: 'Coffre pris dans la neige', 353: 'Tonneau pris dans la neige',
                358: 'Caisse cachée par une planche', 359: 'Bloc de glace suspendu', 36: 'Statue Xélor',
                360: 'Traineau pris dans la neige', 361: 'Banque', 363: 'Arbre calciné couché',
                366: 'Dessin de Koalak', 367: 'Seau de peinture',
                368: 'Canne à pêche plantée dans une caisse', 369: 'Voleur de coquille',
                37: 'Statue Sacrieur', 370: 'Pagure', 371: 'Squelette de matelot pirate',
                373: 'Squelette de capitaine pirate', 374: 'Squelette de pirate sur un tonneau',
                375: 'Barre', 376: 'Voile pirate', 377: 'Bateau détruit', 378: 'Oeuf',
                379: 'Oeuf de volatile cassé', 38: 'Statue à queue pointue', 382: 'Oeuf dans son nid',
                383: 'Oeuf avec marmaille', 384: 'Cocktail', 385: 'Pagaie', 386: 'Bâton avec une corde',
                387: 'Mangeoire', 389: 'Cocktail', 39: 'Statue Pandawa', 394: 'Oeuf de Dragoeuf',
                395: 'Oeuf de volatile', 396: 'Oeuf de Dragoeuf enfoui', 397: 'Oeuf de Dragoeuf cassé',
                398: 'Oeuf surprise', 399: 'Tonneau de tentacules', 40: 'Statue Zobal',
                400: 'Etalage de poisson', 401: 'Poisson suspendu', 402: 'Poisson accroché par la queue',
                403: 'Poisson avec la tête en bas', 404: 'Étendard', 405: 'Etendard avec des os',
                406: 'Etendard avec un seul os', 407: 'Etendard feuillu', 408: 'Dessin',
                409: 'Dessin de Bwork', 41: 'Statue Steamer', 414: 'Ciseaux et peigne',
                415: 'Bouftou suspendu', 416: 'Viande de Bouftou accrochée', 417: 'Fenêtre avec tissu',
                418: 'Seau de sable', 419: 'Coquillage rayé', 42: 'Statue Lhambadda', 420: 'Affiche',
                421: 'Affiche de monstre', 422: 'Affiche de crabe', 423: 'Affiche de nourriture',
                424: 'Crabe effrayant', 425: 'Monstre marin', 426: 'Monstre des profondeurs',
                427: 'Affiche de bateau', 428: 'Piston', 429: 'Menhir', 43: 'Panneau de Kerubim',
                430: "Cible d'un archer talentueux", 431: "Cible d'un archer confirmé",
                434: "Cible d'un archer débutant", 435: 'Tente cornue de Mulou fléché',
                436: 'Coffre enfoui', 437: 'Charrette cassée', 438: 'Observateur furtif', 439: 'Bombarde',
                44: 'Planche', 440: 'Longue vue', 441: 'Trappe', 442: 'Trappe sombre',
                443: 'Trappe sombre à 9 trous', 444: 'Trappe sombre à 16 trous', 445: 'Trappe lumineuse',
                446: 'Trappe lumineuse à 9 trous', 447: 'Trappe lumineuse à 16 trous',
                448: 'Bobine encordée', 449: 'Rouleau de métal posé sur la tranche', 450: 'Robot',
                451: 'Géant de fer', 452: 'Robot avec une pince', 453: 'Robot avec 2 yeux',
                454: 'Robot cassé', 455: 'Visse géante', 456: 'Jardinière', 457: 'Jardinière carrée',
                458: 'Jardinière en engrenage', 459: 'Jardinière en double engrenage',
                46: 'Abreuvoir en pierre', 460: 'Drapeau du Comte', 461: 'Baliste', 462: 'Cible en paille',
                463: 'Quintaine', 464: 'Quintaine Minotoror', 465: 'Minotoror',
                466: 'Quintaine épouvantail', 467: 'Epouvantail', 468: "Ratelier d'armes", 469: 'Epée',
                47: 'Sac', 470: 'Epée prise dans la neige', 472: 'Barricade', 473: 'Main',
                474: 'Etendard de cordonnier', 475: 'Tonneau rempli de lannières de cuir',
                476: 'Rouleau de tissu', 477: 'Tête de Dragon Cochon', 478: 'Deux grosses défenses',
                479: 'Groin de dragon', 48: 'Panneau', 480: 'Pomme fourrée', 481: "Entrée d'égoûts",
                482: 'Entrée malodorante', 483: 'Echelle cassée', 484: 'Sac suspendu', 485: "Seau d'arêtes",
                486: 'Main de monstre', 487: 'Planches suspendues', 488: 'Grande bière',
                489: 'Rouleau de métal', 49: 'Statue', 490: 'Rouleau de métal accroché',
                491: 'Tête de mort en pavés', 492: 'Tofu épinglé', 493: 'Statue impressionante',
                496: 'Monture de pierre', 497: 'Pierre précieuse', 498: 'Maillons', 499: 'Chaîne',
                500: 'Panneau "Alchimistes"', 501: 'Panneau "Bijoutiers"', 502: 'Panneau "Bricoleurs"',
                503: 'Panneau "Boulangers"', 504: 'Panneau "Forgerons"', 505: 'Panneau "Tailleurs"',
                506: 'Panneau "Bouchers"', 507: 'Panneau "Sculpteurs"', 508: 'Panneau "Bûcherons"',
                509: 'Panneau "Eleveurs"', 510: 'Casque', 511: 'Peau étendue', 512: 'Peau de Fricochère',
                513: 'Peau de Givrefoux', 514: 'Tas de peaux', 515: 'Plan de bricolage',
                516: 'Affiche de bricolage', 517: 'Armure', 518: 'Epaulière', 519: 'Casque à plume',
                520: 'Casque à visière', 521: 'Wabbit peintre', 522: 'Wabbit endormi',
                523: 'Wabbit pêcheur', 524: 'Wo Wabbit endormi', 525: 'Wabbits perchés',
                526: 'Foreuse Wabbit', 527: 'Foreuse plantée', 528: 'Etendard Bouftou',
                529: 'Rouleau de laine', 53: 'Outil', 530: 'Sac de laine', 531: 'Bouftou mort',
                532: 'Cible Bouftou', 533: 'Blason en peau', 534: 'Masse', 535: 'Marteau-piqueur',
                536: 'Tonneau de peinture', 537: 'Pinceau usagé', 538: 'Pierres suspendues',
                539: 'Blason Kanigroula', 540: 'Blason Kanigrou', 541: 'Blason trace de patte',
                542: 'Blason ossements', 543: 'Blason longues dents', 544: 'Pendentif de sorcière',
                545: 'Cabane en bois', 546: 'Cabane avec plancher', 547: 'Cabane avec porte en toile',
                548: 'Cabane avec boîte aux lettres', 549: 'Cabane avec toit en toile', 55: 'Pince',
                550: 'Cabane sans plancher', 551: 'Cabane sans toit', 552: 'Totem avec des bois',
                553: 'Citrouille perchée', 554: 'Arbre bonbon', 555: 'Chasse-neige', 556: 'Écharpe',
                557: 'Moulin', 559: "Support d'ailes de moulin", 56: 'Canne à pêche',
                560: 'Moulin sans toit', 561: "Caisse d'outils", 562: 'Bouteille', 563: 'Chapeau',
                564: 'Coiffe', 565: 'Couvre-chef', 566: 'Dora Bora', 567: 'Coiffe du Bouftou',
                568: 'Coiffe du Bouftou royal', 569: 'Krokop', 57: 'Attrape poisson', 570: 'Le Floude',
                571: 'Casque de Maître Nabur', 572: 'Chapeau du marié', 573: 'Couronne du roi Gelax',
                574: "Casque pour l'île de Moon", 575: 'Casque Citrouille', 576: 'Bandeau',
                577: 'Chapeau à plume', 578: 'Branche cassée', 579: 'Ecoulement de sève', 58: 'Tonnelle',
                580: 'Seau suspendu', 581: 'Epée plantée', 582: 'Peluche Koalak',
                583: 'Dessin de Dragodinde', 584: 'Trace de griffes', 585: 'Fissure', 586: 'Rocher fendu',
                587: 'Arbre creux', 588: 'Arbre à feuilles trouées', 589: 'Plante épineuse',
                59: 'Abri en toile', 590: 'Plante carnivore', 592: 'Plante tentaculaire',
                593: 'Plante pomme de pin', 594: 'Souche avec un champignon', 595: 'Rocher sacrificiel',
                596: 'Arbre à lanterne', 597: 'Arbre rempli de crânes', 598: 'Arbre transpercé',
                599: 'Fleur verte', 600: 'Fleur bleue', 601: 'Dalle en forme de Kama',
                602: "Tonneau rempli d'outils", 603: 'Chariot à vapeur', 604: 'Sac de Kamas',
                605: 'Sac de Kamas éventré', 606: "Chariot rempli d'or", 608: 'Sac de Kamas noué',
                609: 'Coffre moustachu', 610: 'Coffre moustachu enfoui', 611: 'Chariot de pierres',
                612: 'Pierre triangulaire', 613: 'Globe étoilé', 614: "Coffre d'amour", 615: 'Dragon en or',
                618: 'Queue de dragon', 619: 'Tonneau de Kamas', 620: 'Statue de Centaure',
                621: 'Bac de laine', 622: 'Dessin de Koalak armé', 623: 'Dessin de squelette Koalak',
                624: 'Lance plantée', 625: 'Panneau "Os"', 626: 'Os en bois', 627: 'Trou',
                628: 'Pierre taillée', 629: "Masse d'armes végétale", 630: 'Fleur spiralée',
                631: 'Rocher sculpté', 632: 'Corbac écrasé', 633: 'Rocher troué', 634: 'Os dessiné',
                636: 'Arche rocheuse', 637: 'Plante éventail', 638: 'Seau renversé', 639: 'Tofu enfourché',
                64: 'Abreuvoir', 640: 'Panneau "Fonderie"', 641: 'Seau de pierres précieuses',
                642: 'Tonneau ficelé', 643: 'Bateau échoué', 644: 'Bateau en papier', 645: 'Bocal',
                646: "Bitte d'amarrage", 647: 'Barque renversée', 648: 'Rafiot renversé',
                649: 'Chaloupe renversée', 65: 'Abreuvoir en bois', 650: 'Barque avec une étoile',
                651: 'Rafiot avec une étoile', 652: 'Chaloupe avec une étoile', 653: 'Charette de céréales',
                654: 'Tracteur', 655: 'Statue de faucheur', 656: 'Sac de charbon', 657: 'Viande suspendue',
                658: 'Saucisse suspendue', 659: 'Souche avec des petites pousses', 66: 'Marteau',
                660: 'Jouet Tofu', 661: 'Jouet Bouftou', 662: 'Arbre à Chacha', 663: 'Griffoir',
                664: 'Roulotte cassée', 665: 'Roulotte transpercée', 666: "Panier d'oeufs",
                667: 'Flèche cassée', 668: 'Feu de camp', 669: 'Aventurier gelé', 67: 'Etoile de mer',
                670: 'Palette en bois', 671: 'Cawotte plantée', 672: 'Coquillage conique',
                673: 'Coquillage spiralé', 674: 'Caisse de boucher', 675: 'Zaapi', 676: 'Ballon',
                677: 'Serviette de plage', 678: 'Cadeau', 680: 'Os pris dans la glace', 681: 'Tube feuillu',
                682: 'Caisse de coraux', 683: 'Carton', 684: 'Rondins de bambou', 686: 'Jarre ouverte',
                687: 'Jarre fermée', 688: 'Tonneau explosif', 689: 'Tonneau flottant',
                690: 'Flèche plantée dans le sol', 691: 'Champignon luminescent', 692: 'Caisse flottante',
                693: 'Bombe', 694: 'Lance', 695: 'Porte-manteau', 696: "Panneau d'affichage",
                697: 'Sac de Tofus', 698: 'Torche', 699: 'Chaîne mouillée',
                70: 'Etoile de mer avec un oeil', 702: 'Porte de cave', 703: 'Réservoir',
                704: 'Chacha noir', 705: 'Pieu avec des os', 706: 'Pot en forme de crâne',
                707: 'Panneau étoilé', 708: 'Poisson toxique', 709: 'Barque au mât cassé',
                71: "Duo d'étoiles de mer", 710: 'Panneau couvert', 711: 'Ballon accroché',
                712: 'Chariot à viande', 713: 'Crâne cornu sur un piquet', 714: 'Panneau avec un oeil',
                715: 'Citerne', 716: "Château d'eau", 717: 'Noix de Kokoko ouverte',
                718: 'Volatile squelette', 719: "Squelette d'humanoïde empalé", 72: 'Sac de farine',
                720: 'Scie', 721: "Trace d'ours", 722: 'Lampadaire en os', 723: 'Tonneau porté',
                724: 'Citrouille gelée', 725: 'Cawotte gelée', 726: 'Drapeau de Vulkania', 727: 'Chaudron',
                728: 'Soutien-gorge', 729: 'Tas de fourrures', 73: 'Sac de boulanger',
                730: 'Squelette sur un banc', 731: 'Cible en forme de maison', 732: 'Sous-vêtement',
                733: 'Culotte', 734: 'Affiche de tortue', 735: 'Epée ensanglantée', 736: 'Barge',
                737: 'Croix lumineuse', 738: 'Crâne de Givrefoux', 739: 'Banc cassé', 74: 'Arrosoir',
                740: 'Crâne peint', 741: "Caisse d'engrenages", 742: 'Chariot de mineur renversé',
                743: 'Centrale thermique', 744: 'Cible en paille sur roulettes', 746: 'Sac de bonbons',
                747: 'Ballon Tofu', 748: 'Ballon Bouftou', 749: 'Boîte à outils', 75: 'Seau',
                750: 'Boîte de pizzas', 751: 'Fosse commune', 752: 'Chevalet',
                753: 'Chariot rempli de charbon', 754: 'Roulotte à jouets', 755: 'Bestiole géante en bois',
                756: 'Chaise de maître nageur', 757: 'Voiture en bois', 758: 'Arrosoir mécanique',
                759: 'Bougeoir en forme de crâne', 76: 'Seau de forgeron', 760: 'Toilettes',
                761: 'Téléscope', 762: 'Charrette à deux roues', 763: 'Charrette à 4 roues',
                764: 'Lance avec des os', 765: "Réservoir d'eau", 766: 'Enclume', 767: 'Drapeau en slip',
                768: 'Statue avec des dagues', 769: 'Caisse mystère', 77: 'Barque', 770: 'Caisse médicale',
                771: 'Seringue géante', 772: 'Flamèche sur un ponton', 773: 'Tronc creux couché',
                774: 'Roue à aube', 775: 'Chacha pris dans une toile', 776: 'Tombe en bois',
                777: 'Grand coquillage', 778: 'Wabbit gelé', 779: 'Piège', 780: 'Cercueil en bois',
                781: 'Broyeur', 782: 'Statue qui pleure', 783: 'Squelette de poisson', 86: 'Pioche',
                87: 'Souche qui ne repousse pas', 89: 'Brouette', 90: 'Eolienne', 905: 'Poupée',
                906: 'Feu éteint', 907: 'Tente de foire', 908: 'Pot en ossements', 909: "Guirlande d'os",
                91: 'Silo', 910: 'Statue Roublard', 911: 'Statue Huppermage', 912: 'Amphore',
                913: 'Champignon sur un arbre', 914: 'Tombe ouverte', 915: 'Cerceuil enfoui',
                916: 'Tambour', 917: 'Roulotte carbonisée', 918: 'Roulotte brûlée', 919: 'Roulotte fumante',
                92: 'Ballot de paille', 920: 'Statue de crabe', 921: 'Squelette de Droupik',
                922: 'Caisse cassée', 923: 'Coffre recouvert de mousse', 924: 'Chacha noir assommé',
                925: 'Cage avec une goule', 926: 'Tente détruite', 927: 'Tonneau détruit',
                928: 'Tonneau enfoui', 929: 'Roulotte laboratoire',
                93: 'Ballot de paille sur une charrette', 930: 'Roulotte enfouie', 931: 'Borne',
                932: 'Borne enfouie', 933: 'Squelette de mineur', 934: 'Goule empalée',
                935: 'Fontaine sanguinolente', 936: 'Goule pendue', 937: "Squelette d'humanoïde encordé",
                938: 'Likrone', 939: 'Goule coincée', 94: 'Parasol', 940: 'Butoir en os',
                941: 'Tombe Ouginak', 942: 'Statue Ouginak', 943: 'Monocycle', 944: "Pyramide d'os",
                945: 'Canon en bois', 946: 'Ballon crapaud', 947: 'Ballon Dragodinde',
                948: 'Roulotte fongique', 949: "Statue d'Ougah", 950: 'Statue de champignon',
                951: 'Statue fongique', 952: 'Champignon en pierre', 953: 'Os avec un boulet',
                954: 'Echelle en os', 955: 'Coffre porté par un Pandawa', 956: 'Pompe géante',
                957: 'Bicyclette', 958: 'Piège à mâchoire', 959: 'Statue avec un trident',
                960: "Peau d'Ecaflip", 961: 'Peau de Kanigrou', 962: 'Tuyau géant', 99: 'Nichoir de Piou'}[id]

class HintList:
    hints: List[Hint]

    def __init__(self, hints: List[Hint]) -> None:
        self.hints = hints

    @staticmethod
    def from_dict(obj: Any) -> 'HintList':
        assert isinstance(obj, dict)
        hints = from_list(Hint.from_dict, obj.get("hints"))
        return HintList(hints)

    @staticmethod
    def from_url(url: str) -> 'HintList':
        resp = requests.get(url)
        return HintList.from_dict((json.loads(resp.content)))

    @staticmethod
    def from_url_parameters(pos_x: int, pos_y: int,direction: Direction,world: int ) -> 'HintList':
        url = "https://dofus-map.com/huntTool/getData.php?x="+str(pos_x)+"&y="+str(pos_y)+"&direction="+direction.value+"&world="+str(world)+"&language=fr"
        return HintList.from_url(url)




