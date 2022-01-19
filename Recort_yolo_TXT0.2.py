'''
Data criação: 25/10/2021 || Data modificação: 03/12/2021
O Código realiza recorte das imagens com base nos rotulos criados no labelImg, e salva em uma pasta com o codigo da classe.
Autor: Hércules Carlos
Versão: 0.2v
'''
import cv2
from matplotlib import pyplot as plt
from os import chdir,listdir, getcwd, mkdir, path
import fileinput #biblioteca para remover linha vazia

#path local (pega o camingo da pasta atual do programa)
get_root = getcwd()

#Nomalizar path local para unix path
Norm_root = get_root.replace('\\', '/')

'''Camindo das imagens'''
Image = Norm_root + '/Image'

'''Caminho dos rotulos'''
Rotulo = Norm_root + '/Rotulo'
'''pasta output para salvar os arquivos'''
Output = Norm_root + '/Output'

'''local onde esta armazenado os input'''
directoryImg = listdir(Image)
directoryR = listdir(Rotulo)
chdir(Norm_root)


'''ordenando listas com os nomes das imagens e rolutos'''
#é importante para manter tanto rotulo quanto imagem na mesma ordem
directoryImgSort = (sorted(directoryImg))
directoryRSort = (sorted(directoryR))

'''Vetores para guardar o nome das imagens e dos Label'''
NameLabel = []
NameImage = []
    
    
'''armazena os nomes dos arquivos que contem os rotulos no vetor NameLabel[]'''
for NameArq in directoryRSort:
    #ordenar por nome
    NameLabel.append('Rotulo/'+NameArq)
#print(NameLabel)

'''#armazena os nomes das imagem no vetor NameImage[]'''   
for NameImg in directoryImgSort:
    #ordenar por nome
    NameImage.append('Image/'+NameImg)
#print(NameImage)                     

    
'''fucao Separa_cordenada1('nome da imagem')-> um vetor com as ['rotulo', 'cordenada1', 'cirdenada2', 'cordenad3', 'cordenada4'] a linha das coordenadas'''
def Separa_cordenada3(ArchiveName):
    Archive = open(ArchiveName, 'r')
    cordenadas = []
    armaz_cord = []
    for linhas in Archive:
        if linhas != None:
            cordenadas.append(str(linhas))
            
    #print(cordenadas.pop())
    #print(cordenadas)
    
        
    for line in cordenadas:
        cordenada = line[3:38]
        c0 = int(line[:2])
        c1 = float(cordenada[:8])
        c2 = float(cordenada[9:8+9])
        c3 = float(cordenada[18:16+10])
        c4 = float(cordenada[27:24+11])
        codigo = [c0,c1,c2,c3,c4]

        armaz_cord.append(codigo)

    #ira returno um vetoro com todas as coordenadas por uma linha
    return armaz_cord

    #fechar arquivo   
    Archive.close()


        
'''funcao que carrega imagem imagem(nome)-> retorna imagem em RGB'''
def imagem(nome_imagem):
    img = cv2.imread(nome_imagem)
    img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    return img_rgb

'''salvar a imagem Save(nome.jpg', numero_classe[n], /caminho/, matriz da Imagem)'''   
def creat_save(nome,classe,caminho, image):
    saveLocal = caminho+'/'+str(classe)+'/'+nome
    cv2.imwrite(saveLocal,image)
    

'''funcao recorte crop('Image Matrix', Cordenadas [0, 0.0, 0.0, 0.0]) -> retorna a imagem recortada em rgb'''
def crop(Mx_img, codigo):
    
    #return img
    height, width, _ = Mx_img.shape   
    
    #centro da imagem
    center_x = int(codigo[1] * width)
    center_y = int(codigo[2] * height)
            
    w = int(codigo[3] * width)
    h = int(codigo[4] * height)
    x = int(center_x - (w / 2))
    y = int(center_y - (h / 2))

    w1 = x+w
    h1 = y+h
    
    #recorte
    crop_img = Mx_img[y:h1, x:w1]
    crop_imgRgb = cv2.cvtColor(crop_img,cv2.COLOR_BGR2RGB)
    return crop_imgRgb


'''Cria todas pasta com o numero do vetor create_drectory(n)'''
def create_drectory (vetor_class):
    pastas = []
    archive_class = open(vetor_class, 'r')
    for line in archive_class:
        pastas.append(line)
    for i in range(len(pastas)):
        mkdir(Output + '/' + str(i))
    
    

'''checar se o diretorio existe'''
#vetor que guarda os nomes das classes
archive = []
#abrir arquivo classes.txt modo leitura
archive_class = open(get_root+'/'+'classes.txt', 'r')

#adiciona as classes ao vetor archive[]
for line in archive_class:
    archive.append(line)
    
for i in range(len(archive)):
    
    if path.isdir(Output+'/'+str(i)):
        #checar se o diretorio existe
        pass
    else:
        #se diretonio não existir crie diretorio com o numero da classe
        create_drectory(get_root+'/'+'classes.txt')
        print("Todos os diretórios foram criados!")

  
    
'''Main'''
#percorre de acordo com a quantidade de rotulos
#desta forma o codigo so abre a imagem que possui o rotulo
for i in range(len(NameLabel)):
    #carregar as imagens
    img = imagem(NameImage[i])
    
    #coordenada (retorna a classe as coordenas dos rotulos [1,0.0, 0.0, 0.0, 0.0])
    coord = Separa_cordenada3(NameLabel[i])
    
    #realiza o recorte de cada coordenada armazenada no arquivo txt e salva na respectiva pasta
    for j in range(len(coord)):
        #print(coord[0][0])
        corte = crop(img, coord[j])
        #print(coord[j])

        #Armazena o nome da imagem
        nome = 'ctnr '+'('+str(i)+').jpg'

        #salve (nome, cordenada, caminho de saida, Matriz_image)
        creat_save(nome,coord[j][0],Output, corte)

  
print('Fim da execução!!')

    

