import { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Bot, User, Send, ThumbsUp, ThumbsDown } from 'lucide-react';
import './App.css';

function App() {
  const [pergunta, setPergunta] = useState('');
  const [carregando, setCarregando] = useState(false);
  const [mensagens, setMensagens] = useState([
    {
      role: 'assistant',
      content: '🤖 **Olá! Sou o Assistente de Inteligência Artificial do Neo Bank.** \n\nEstou aqui para tirar suas dúvidas sobre nossas políticas internas, processos e documentações operacionais. Como posso ajudar você hoje?'
    }
  ]);

  const enviarPergunta = async (e) => {
    e.preventDefault();
    if (!pergunta.trim()) return;

    const novaPergunta = pergunta;
    setPergunta('');
    setMensagens((prev) => [...prev, { role: 'user', content: novaPergunta }]);
    setCarregando(true);

    try {
      // Faz a requisição para a nossa API em Python (FastAPI)
      const resposta = await axios.post('/api/perguntar', {
        pergunta: novaPergunta
      });

      setMensagens((prev) => [
        ...prev,
        { role: 'assistant', content: resposta.data.resposta }
      ]);
    } catch (erro) {
      console.error('Erro na requisição:', erro);
      setMensagens((prev) => [
        ...prev,
        { role: 'assistant', content: '❌ Desculpe, ocorreu um erro ao conectar com os servidores internos. Tente novamente em instantes.' }
      ]);
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="app-container">
      <header className="cabecalho">
        <h1>🏢 Portal Corporativo | Agente IA</h1>
        <p>Base de Conhecimento Oficial - Neo Bank</p>
      </header>

      <main className="chat-container">
        <div className="historico">
          {mensagens.map((msg, index) => (
            <div key={index} className={`mensagem-wrapper ${msg.role}`}>
              <div className="icone-perfil">
                {msg.role === 'assistant' ? <Bot size={24} /> : <User size={24} />}
              </div>
              <div className="balao-mensagem">
                <ReactMarkdown>{msg.content}</ReactMarkdown>
                
                {/* Exibe botões de feedback apenas nas respostas da IA */}
                {msg.role === 'assistant' && index !== 0 && (
                  <div className="feedback-container">
                    <span>A resposta foi útil?</span>
                    <button className="btn-feedback"><ThumbsUp size={16} /></button>
                    <button className="btn-feedback"><ThumbsDown size={16} /></button>
                  </div>
                )}
              </div>
            </div>
          ))}
          {carregando && (
            <div className="mensagem-wrapper assistant">
              <div className="icone-perfil"><Bot size={24} /></div>
              <div className="balao-mensagem digitando">Consultando documentos internos...</div>
            </div>
          )}
        </div>

        <form onSubmit={enviarPergunta} className="area-input">
          <input
            type="text"
            value={pergunta}
            onChange={(e) => setPergunta(e.target.value)}
            placeholder="Ex: Como funciona o reembolso de viagens?"
            disabled={carregando}
          />
          <button type="submit" disabled={carregando || !pergunta.trim()}>
            <Send size={20} />
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;