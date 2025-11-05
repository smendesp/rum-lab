import asyncio
import time


async def tarefa_demorada(nome, segundos):
    print(f'Iniciando {nome}...')
    await asyncio.sleep(segundos)
    print(f'Finalizando {nome} após {segundos} segundos')
    return f'Resultado de {nome}'


async def main():
    # Criando tarefa sem esperar
    task = asyncio.create_task(tarefa_demorada('Tarefa Async', 3))

    print('Continuando execução...')
    # Fazendo outras coisas
    await asyncio.sleep(1)
    print('Fazendo outras tarefas...')

    # Se quiser esperar eventualmente:
    # resultado = await task


asyncio.run(main())
