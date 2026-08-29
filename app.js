const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const { v4: uuidv4 } = require('uuid');
const moment = require('moment');
const app = express();
const PORT = process.env.PORT || 3000;

// ==========================================
// MIDDLEWARES
// ==========================================
app.use(helmet());
app.use(cors());
app.use(express.json());

// ==========================================
// BANCO DE DADOS EM MEMÓRIA (simulado)
// ==========================================
const db = {
  propostas: [],
  analises: [],
  execucoes: [],
  gruposMonitorados: [],
  webhooks: []
};

// ==========================================
// MÓDULO 1: VIGILANTE 🕵️
// ==========================================
class Vigilante {
  constructor() {
    this.gruposAtivos = [
      { nome: 'Marketing Digital BR', membros: 45000, engajamento: 8.5, horarioPico: '10:00' },
      { nome: 'Vendas Online', membros: 28000, engajamento: 6.2, horarioPico: '14:00' },
      { nome: 'Empreendedores BR', membros: 52000, engajamento: 7.8, horarioPico: '09:00' },
      { nome: 'Tráfego Pago', membros: 32000, engajamento: 9.1, horarioPico: '20:00' },
      { nome: 'Infoprodutores', membros: 19000, engajamento: 8.9, horarioPico: '16:00' }
    ];
    this.tendencias = [
      'Vídeos curtos (30-60s) geram 3x mais engajamento',
      'Posts com perguntas têm 40% mais comentários',
      'Carrosséis convertem 2x mais que imagens únicas',
      'Reels estão com alcance orgânico recorde'
    ];
  }

  monitorarGrupos() {
    const analise = this.gruposAtivos.map(grupo => ({
      ...grupo,
      pontuacao: (grupo.engajamento * (grupo.membros / 10000)).toFixed(2),
      recomendacao: grupo.engajamento > 7 ? 'ALTO POTENCIAL' : 'MONITORAR',
      ultimaAtualizacao: moment().format('DD/MM/YYYY HH:mm:ss')
    }));
    db.gruposMonitorados = analise;
    return analise;
  }

  getTendencias() {
    return this.tendencias;
  }

  // Simula recebimento de webhook do Groups Watcher
  receberWebhook(dados) {
    const evento = {
      id: uuidv4(),
      ...dados,
      recebidoEm: moment().toISOString()
    };
    db.webhooks.push(evento);
    return evento;
  }

  getWebhooks() {
    return db.webhooks.slice(-20);
  }
}

// ==========================================
// MÓDULO 2: ESTRATEGISTA 🧠
// ==========================================
class Estrategista {
  gerarInsights(dadosGrupos) {
    const melhoresGrupos = dadosGrupos
      .filter(g => g.pontuacao > 7)
      .sort((a, b) => b.pontuacao - a.pontuacao);

    const insights = {
      melhoresGrupos: melhoresGrupos.slice(0, 3),
      totalGrupos: dadosGrupos.length,
      mediaEngajamento: (dadosGrupos.reduce((acc, g) => acc + parseFloat(g.pontuacao), 0) / dadosGrupos.length).toFixed(2),
      horarioRecomendado: this._calcularMelhorHorario(dadosGrupos),
      estrategiaSugerida: this._definirEstrategia(dadosGrupos),
      timestamp: moment().toISOString()
    };
    db.analises.push(insights);
    return insights;
  }

  _calcularMelhorHorario(grupos) {
    const horarios = grupos.map(g => g.horarioPico);
    const maisFrequente = horarios.sort((a, b) =>
      horarios.filter(v => v === a).length - horarios.filter(v => v === b).length
    ).pop();
    return maisFrequente || '10:00';
  }

  _definirEstrategia(grupos) {
    const media = grupos.reduce((acc, g) => acc + parseFloat(g.pontuacao), 0) / grupos.length;
    if (media > 8) return 'ATAQUE - Público altamente engajado';
    if (media > 6) return 'CONSTRUÇÃO - Aumentar presença gradualmente';
    return 'TESTE - Público frio, precisa aquecer';
  }

  getHistorico() {
    return db.analises.slice(-10);
  }
}

// ==========================================
// MÓDULO 3: PROPOSITOR 📋
// ==========================================
class Propositor {
  gerarProposta(insights, tipoAcao = null) {
    const tiposAcao = ['video', 'imagem', 'carrossel', 'enquete', 'texto'];
    const acaoSelecionada = tipoAcao || tiposAcao[Math.floor(Math.random() * tiposAcao.length)];

    const proposta = {
      id: uuidv4(),
      acao: acaoSelecionada,
      local: insights.melhoresGrupos?.[0]?.nome || 'Grupo Recomendado',
      motivo: insights.estrategiaSugerida || 'Baseado em análise de dados',
      horarioSugerido: insights.horarioRecomendado || '10:00',
      status: 'aguardando_autorizacao',
      prioridade: insights.melhoresGrupos?.length > 0 ? 'ALTA' : 'MÉDIA',
      criadoEm: moment().toISOString(),
      validoAte: moment().add(24, 'hours').toISOString()
    };

    db.propostas.push(proposta);
    return proposta;
  }

  getPendentes() {
    return db.propostas.filter(p => p.status === 'aguardando_autorizacao');
  }

  getTodas() {
    return db.propostas.slice(-20);
  }
}

// ==========================================
// MÓDULO 4: EXECUTOR ⚡
// ==========================================
class Executor {
  executarAcao(propostaId, autorizado = false) {
    const proposta = db.propostas.find(p => p.id === propostaId);
    
    if (!proposta) {
      return { erro: 'Proposta não encontrada', status: 'falha' };
    }

    if (proposta.status !== 'aguardando_autorizacao') {
      return { erro: 'Proposta já foi processada', status: 'falha' };
    }

    if (!autorizado) {
      proposta.status = 'rejeitada';
      return { mensagem: 'Ação não autorizada', proposta, status: 'rejeitada' };
    }

    const resultado = {
      id: uuidv4(),
      propostaId: proposta.id,
      acao: proposta.acao,
      local: proposta.local,
      status: 'executada',
      resultado: 'Sucesso',
      detalhes: {
        alcanceEstimado: `${Math.floor(Math.random() * 5000) + 1000} pessoas`,
        engajamento: `${(Math.random() * 15 + 5).toFixed(1)}%`,
        cliques: Math.floor(Math.random() * 200) + 20
      },
      executadoEm: moment().toISOString()
    };

    proposta.status = 'executada';
    db.execucoes.push(resultado);
    return resultado;
  }

  relatorioDesempenho() {
    const total = db.execucoes.length;
    const sucessos = db.execucoes.filter(e => e.status === 'executada').length;
    return {
      totalExecucoes: total,
      taxaSucesso: total > 0 ? ((sucessos / total) * 100).toFixed(2) + '%' : '0%',
      ultimasExecucoes: db.execucoes.slice(-5),
      timestamp: moment().toISOString()
    };
  }

  getHistorico() {
    return db.execucoes.slice(-20);
  }
}

// ==========================================
// INSTANCIAR MÓDULOS
// ==========================================
const vigilante = new Vigilante();
const estrategista = new Estrategista();
const propositor = new Propositor();
const executor = new Executor();

// ==========================================
// ROTAS - MÓDULO VIGILANTE 🕵️
// ==========================================
app.get('/api/vigilante/grupos', (req, res) => {
  const resultado = vigilante.monitorarGrupos();
  res.json({ status: 'sucesso', dados: resultado, total: resultado.length });
});

app.get('/api/vigilante/tendencias', (req, res) => {
  res.json({ status: 'sucesso', dados: vigilante.getTendencias() });
});

app.post('/api/vigilante/webhook', (req, res) => {
  const evento = vigilante.receberWebhook(req.body);
  res.json({ status: 'sucesso', dados: evento, mensagem: 'Webhook recebido!' });
});

app.get('/api/vigilante/webhooks', (req, res) => {
  res.json({ status: 'sucesso', dados: vigilante.getWebhooks() });
});

// ==========================================
// ROTAS - MÓDULO ESTRATEGISTA 🧠
// ==========================================
app.post('/api/estrategista/insights', (req, res) => {
  const dadosGrupos = vigilante.monitorarGrupos();
  const resultado = estrategista.gerarInsights(dadosGrupos);
  res.json({ status: 'sucesso', dados: resultado });
});

app.get('/api/estrategista/historico', (req, res) => {
  res.json({ status: 'sucesso', dados: estrategista.getHistorico() });
});

// ==========================================
// ROTAS - MÓDULO PROPOSITOR 📋
// ==========================================
app.post('/api/propositor/gerar', (req, res) => {
  const { tipoAcao } = req.body;
  const insights = estrategista.gerarInsights(vigilante.monitorarGrupos());
  const resultado = propositor.gerarProposta(insights, tipoAcao);
  res.json({
    status: 'sucesso',
    dados: resultado,
    mensagem: 'Proposta gerada. Aguardando sua autorização.'
  });
});

app.get('/api/propositor/pendentes', (req, res) => {
  const pendentes = propositor.getPendentes();
  res.json({ status: 'sucesso', dados: pendentes, total: pendentes.length });
});

app.get('/api/propositor/todas', (req, res) => {
  res.json({ status: 'sucesso', dados: propositor.getTodas() });
});

// ==========================================
// ROTAS - MÓDULO EXECUTOR ⚡
// ==========================================
app.post('/api/executor/autorizar', (req, res) => {
  const { propostaId, autorizado } = req.body;
  if (!propostaId) {
    return res.status(400).json({ erro: 'propostaId é obrigatório' });
  }
  const resultado = executor.executarAcao(propostaId, autorizado);
  res.json({
    status: 'sucesso',
    dados: resultado,
    mensagem: autorizado ? '✅ Ação autorizada e executada!' : '❌ Ação rejeitada.'
  });
});

app.get('/api/executor/relatorio', (req, res) => {
  res.json({ status: 'sucesso', dados: executor.relatorioDesempenho() });
});

app.get('/api/executor/historico', (req, res) => {
  res.json({ status: 'sucesso', dados: executor.getHistorico() });
});

// ==========================================
// DASHBOARD COMPLETO 📊
// ==========================================
app.get('/api/dashboard', (req, res) => {
  const grupos = vigilante.monitorarGrupos();
  const insights = estrategista.gerarInsights(grupos);
  const pendentes = propositor.getPendentes();
  
  res.json({
    status: 'sucesso',
    dados: {
      gruposMonitorados: grupos.length,
      insights: insights,
      propostasPendentes: pendentes.length,
      ultimaProposta: db.propostas.slice(-1)[0] || null,
      desempenho: executor.relatorioDesempenho(),
      tendencias: vigilante.getTendencias(),
      webhooksRecebidos: db.webhooks.length
    },
    timestamp: moment().toISOString()
  });
});

// ==========================================
// ROTAS BÁSICAS
// ==========================================
app.get('/', (req, res) => {
  res.json({
    nome: 'Perito Virtual Facebook',
    versao: '2.0.0',
    status: 'online',
    descricao: 'Agente autônomo especialista em vendas orgânicas no Facebook',
    modulos: ['Vigilante', 'Estrategista', 'Propositor', 'Executor'],
    rotas: {
      vigilante: '/api/vigilante/grupos, /api/vigilante/tendencias, /api/vigilante/webhook',
      estrategista: '/api/estrategista/insights, /api/estrategista/historico',
      propositor: '/api/propositor/gerar, /api/propositor/pendentes, /api/propositor/todas',
      executor: '/api/executor/autorizar, /api/executor/relatorio, /api/executor/historico',
      dashboard: '/api/dashboard'
    },
    timestamp: moment().toISOString()
  });
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: moment().toISOString() });
});

// ==========================================
// INICIAR SERVIDOR
// ==========================================
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🕵️ Perito Virtual Facebook V2.0`);
  console.log(`📡 Rodando em http://localhost:${PORT}`);
  console.log(`📊 Dashboard: http://localhost:${PORT}/api/dashboard`);
  console.log(`✅ Servidor pronto para receber requisições!`);
});

module.exports = app;
