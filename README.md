# ProjEvolutivos
Projeto da disciplina Sistemas Evolutivos Aplicados a Robotica

Algoritmo evolutivo para resolução de labirintos.
Para executar: `python main.py`

O aplicativo pode ser configurado pelo arquivo `settings.py`:
- maze_size: número de nós para o algoritmo de geração do labirinto
- seed: seed para o rng do gerador
- num: define o número de indivíduos
- elite_ratio: define a proporção de indivíduos que serão considerados como 'melhores'
- mutation_factor: define a chance de adicionar um novo elemento, alterar o último elemento e remover o último elemento do caminho de um indivíduo
- predate_every: define o intervalo para realizar a predação, ou None para desativar

Requerimentos:
- python 3.9
- NumPy (para instalar `pip install numpy`)
- Matplotlib (para instalar `pip install matplotlib`)
