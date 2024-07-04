document.addEventListener('DOMContentLoaded', function() {
    // Lógica para redirecionar para a página de transferência
    const transferButton = document.getElementById('transferButton');
    transferButton.addEventListener('click', function() {
        window.location.href = '/transferencia';
    });

    // Lógica para redirecionar para a página de depósito
    const depositButton = document.getElementById('depositButton');
    depositButton.addEventListener('click', function() {
        window.location.href = '/deposito_page'; // Redireciona para a página de depósito
    });

    // Lógica para redirecionar para a página de saque
    const saqueButtons = document.querySelectorAll('[data-conta]');
    saqueButtons.forEach(button => {
        button.addEventListener('click', function() {
            const numeroConta = button.getAttribute('data-conta');
            window.location.href = `/saque_page?numero_conta=${numeroConta}`;
        });
    });

    // Lógica para o botão de logout
    const logoutButton = document.getElementById('logoutButton');
    logoutButton.addEventListener('click', function() {
        fetch('/logout', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Exibe a mensagem de logout bem-sucedido
            window.location.href = '/'; // Redireciona para a página inicial
        })
        .catch(error => {
            console.error('Erro ao fazer logout:', error);
        });
    });
});
