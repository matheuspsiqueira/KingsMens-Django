// Event listener para o campo de CEP
document.getElementById('cep').addEventListener('blur', function () {
    var cep = this.value.replace(/\D/g, ''); // Remove caracteres não numéricos

    // Verifica se o CEP possui 8 dígitos
    if (cep.length === 8) {
        // Faz a requisição à API ViaCEP
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
            .then(response => response.json())
            .then(data => {
                // Preenche automaticamente os campos de endereço
                document.getElementById('address').value = data.logradouro;
                document.getElementById('city').value = data.localidade;
                document.getElementById('neighborhood').value = data.bairro;
            })
            .catch(error => console.error('Erro ao obter dados do CEP:', error));
    }
});

