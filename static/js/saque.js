document.addEventListener('DOMContentLoaded', function() {
    const saqueForm = document.getElementById('saqueForm');
    const messageDiv = document.getElementById('message');
    const numeroContaInput = document.getElementById('numeroConta');
    const accountNumberElement = document.getElementById('accountNumber');
    const homeButton = document.getElementById('homeButton');

    // Obter parâmetros da URL
    const urlParams = new URLSearchParams(window.location.search);
    const numeroConta = urlParams.get('numero_conta');

    // Exibir o número da conta na página
    if (numeroConta) {
        numeroContaInput.value = numeroConta;
        accountNumberElement.textContent = `Conta: ${numeroConta}`;
    }

    // Lógica para submissão do formulário
    saqueForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(saqueForm);
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });

        fetch('/saque', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
        })
        .then(response => response.json())
        .then(data => {
            messageDiv.innerHTML = `<p>${data.message}</p>`;
            // Aqui você pode redirecionar o usuário ou fazer outras ações conforme necessário
        })
        .catch(error => {
            console.error('Erro ao realizar o saque:', error);
            messageDiv.innerHTML = '<p>Ocorreu um erro ao processar o saque. Tente novamente mais tarde.</p>';
        });
    });

    // Lógica para o botão de voltar para home
    homeButton.addEventListener('click', function() {
        window.location.href = '/home';
    });
});
