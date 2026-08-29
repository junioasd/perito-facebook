const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.json({
    nome: 'Perito Virtual Facebook',
    status: 'online',
    versao: '1.0.0',
    mensagem: 'Servidor rodando com sucesso! 🚀'
  });
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ Perito Virtual rodando na porta ${PORT}`);
});
