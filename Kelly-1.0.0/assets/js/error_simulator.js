// Tentativa de usar uma variável que não existe
async function simularErroReferencia() {
    try {
        console.log(variavelInexistente);
    } catch (error) {
        console.error(error);
        // Retornar valor padrão para continuar
        return false;
    }

}

// Tentativa de chamar método em valor null/undefined
async function simularErroTipo() {
    try {
        console.log('Iniciando simulação de erro do tipo simularErroTipo');
        const objeto = null;
        objeto.metodoInexistente();
    } catch (error) {
        console.error(error);
        // Retornar valor padrão para continuar
        return false;
    }

}

// Código com sintaxe inválida
async function simularErroSintaxe() {
    try {
        console.log('Iniciando simulação de erro do tipo simularErroSintaxe');
        const x = 10
        const y = 20
        console.log(x + y) // Falta ponto e vírgula (em modo estrito)
    } catch (error) {
        console.error(error);
        // Retornar valor padrão para continuar
        return false;
    }

}

// Array com tamanho inválido
async function simularErroRange() {
    try {
        console.log('Iniciando simulação de erro do tipo simularErroRange');
        const array = new Array(-1);
        console.log(array);
    } catch (error) {
        console.error(error);
        // Retornar valor padrão para continuar
        return false;
    }
}

// Tentativa de fazer requisição para URL inexistente
async function simularErroRequisicao() {
    console.log('Iniciando simulação de erro do tipo simularErroRequisicao');
    try {
        const response = await fetch('https://url-inexistente-exemplo.com/api');
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error('Erro na requisição:', error);
        throw error; // Propaga o erro
    }
}

// Promise que sempre rejeita
async function simularErroPromise() {
    console.log('Iniciando simulação de erro do tipo simularErroPromise');
    try {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                reject(new Error('Falha simulada na promise'));
            }, 1000);
        });
    } catch (error) {
        console.error(error);
        // Retornar valor padrão para continuar
        return false;
    }

}


// Lançando erro personalizado
async function simularErroPersonalizado() {
    try {
        console.log('Iniciando simulação de erro do tipo simularErroPersonalizado');
        throw new Error('Este é um erro personalizado para testes');
    } catch (error) {
        console.error(error);
        throw error; // Propaga o erro}        
    }
}


function callErrorSimulator() {

    var callError = Math.floor(Math.random() * 7);

    if (callError === 0) {
        simularErroReferencia();
    } else if (callError === 1) {
        simularErroTipo();
    } else if (callError === 2) {
        simularErroSintaxe();
    } else if (callError === 3) {
        simularErroRange();
    } else if (callError === 4) {
        simularErroRequisicao();
    } else if (callError === 5) {
        simularErroPromise()
            .then(result => console.log(result))
            .catch(error => console.error('Erro capturado:', error));

    } else if (callError === 6) {
        try {
            simularErroPersonalizado();
        } catch (error) {
            console.error('Erro capturado:', error.message);
        }
    }
}

function callErrors() {
    var numberOfError = Math.floor(Math.random() * 7);

    for (var i = 0; i < numberOfError; i++) {
        callErrorSimulator();
    }
}


callErrors();
