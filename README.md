# **Victor Pla i Sanchis**
#### _Doble interpret JSBach_
###### 23-05-2022


![N|Solid](https://raw.githubusercontent.com/jordi-petit/lp-jsbach-2022/main/firma.png)

---------------

#### Descripcio

En aquest projecte trobareu el doble interpret creat per Victor Pla i Sanchis. En el directori dentrega hi han els fitxers: jsbach.py, jsbach.g4, README.md i els tests test-*.jsb.
- **jsbach.py**: conte tot el codi del doble interpret, la classe EvalVisitor, JSBachException i metodes per a la generacio de la musica.
- **jsbach.g4**: conte tota la definicio de la gramatica del doble interpret.
- **README.md**: aquest mateix fitxer.
- **test-merge-sort.jsb**: un fitxer amb extensio _.jsb_ que permet testejar el funcionament de les llistes (amb daltres coses) executant un merge sort. Ordena una llista totalment desordenada del 51 al 0, daquesta manera podem sentir si la llista esta ben ordenada reproduint cada element del vector al final del programa com si de notes es tractessin.


---------------
#### Dependencies
##### Unix

Sempre es recomanable actualitzar les comandes basiques:
```sh
sudo apt update
sudo apt upgrade
```
Python3 per a lexecucio del doble interpret:
```sh
sudo apt install python3
```
Seguidament instalem: lilypond (per a la generacio de musica en _.mid_ i del fitxer _.pdf_ de la corresponent partitura), timidity (per a la conversio de _.mid_ a  _.wav_) i finalment ffmpeg (per a la conversio de _.mid_ a _.mp3_):
```sh
sudo apt install lilypond
sudo apt install timidity
sudo apt install ffmpeg
```

##### Windows

En aquest cas s'ha d'instalar una terminal d'Ubuntu desde la tenda de microsoft (descargada per defecte al OS) i seguir els pasos dinstalacio de Unix. 

##### MacOS

No ho se, no tinc MacOS...


---------------
#### Usage

Per fer us del doble interprat primer lhem de compilar amb la comanda:
```sh
antlr4 -Dlanguage=Python3 -no-listener -visitor jsbach.g4
```
Un cop compilat, podem executar el doble interpret de les seguents maneres:
1. Per a una execucio dun programa anomenat _code.jsb_ amb main podem executar:
```sh
python3 jsbach.py code.jsb
```
**IMPORTANT:** Un cop acabada lexecucio del programa ens deixara visualitzar loutput abans de crear la musica (ja que la generacio de la musica embruta la nostre terminal i pot impedir veure que printeja el programa _.jsb_) i un cop donat a enter o a qualsevol tecla sens generara la musica si existeix.
2. Per a una execucio dun programa anomenat _code.jsb_ amb un metode diferent al Main anomenat Foo amb 3 parametres podem executar (el numero de parametres es indefinit):
```sh
python3 jsbach.py code.jsb Foo param1 param2 param3
```
3. Per a una execucio dun programa anomenat _code.jsb_ amb una generacio de musica amb tempo diferent de 120, per exemple 240, podem executar:
```sh
python3 jsbach.py code.jsb -t 420
```
4. **IMPORTANT:** Per a una execucio dun programa anomenat _code.jsb_ amb una versio de lilypond diferent a 2.14.1 (es la que a mi mha funcionat) podem executar:
```sh
python3 jsbach.py code.jsb -v 2.22.0
python3 jsbach.py code.jsb -v X.X.X
```

---------------
#### Tests interessants
#
Per executar el test del merge-sort doncs executarem:
```sh
python3 jsbach.py test-merge-sort.jsb
```
Recomano accelerar el tempo per a un resultat mes elegant de la seguent manera:
```sh
python3 jsbach.py test-merge-sort.jsb -t 1000
```

Tot i aixo, loutput desitjat per terminal del programa _.jsb_ es el seguent:
```python
Initial list: [51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
Sorted list: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]
Sha comprobat que esta ordenat!

Program ended, press any key to generate the music...
```

---------------
#### Altres

En aquest cas, no hem generat cap extensio extra menos en la creacio de loperador ':' que concatena dues llistes. Ens hem regit en les necessitats minimes que ens demanava lassignatura de LP.
