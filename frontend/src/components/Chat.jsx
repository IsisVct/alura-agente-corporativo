import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

export default function Chat() {
  const [pergunta, setPergunta] = useState('');
  const [mensagens, setMensagens] = useState([
    {
      tipo: 'assistente',
      texto: 'Olá! Sou o Assistente Virtual Corporativo do Neo DB. Como posso ajudar você hoje?'
    }
  ]);
  const [carregando, setCarregando] = useState(false);
  const fimDoChatRef = useRef(null);

  // Auto-scroll para a última mensagem
  useEffect(() => {
    fimDoChatRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [mensagens, carregando]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!pergunta.trim() || carregando) return;

    const textoUsuario = pergunta;
    setPergunta('');
    
    // Adiciona a mensagem do usuário no chat
    setMensagens((prev) => [...prev, { tipo: 'usuario', texto: textoUsuario }]);
    setCarregando(true);

    try {
      // Requisição para a sua API FastAPI
      const respostaApi = await axios.post('http://localhost:8000/api/perguntar', {
        pergunta: textoUsuario
      });

      setMensagens((prev) => [
        ...prev,
        { tipo: 'assistente', texto: respostaApi.data.resposta }
      ]);
    } catch (error) {
      setMensagens((prev) => [
        ...prev,
        { 
          tipo: 'assistente', 
          texto: '⚠️ Desculpe, ocorreu um erro de conexão ao processar sua requisição no Neo DB.' 
        }
      ]);
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-900 text-slate-100 font-sans">
      {/* Header do Sistema */}
      <header className="bg-slate-800 border-b border-slate-700 px-6 py-4 flex items-center justify-between shadow-md">
        <div className="flex items-center space-x-3">
          <div className="w-3 h-3 bg-emerald-500 rounded-full animate-pulse"></div>
          <h1 className="text-lg font-bold tracking-wide text-white">Neo DB • Assistente Corporativo</h1>
        </div>
        <span className="text-xs bg-slate-700 px-3 py-1 rounded-full text-slate-300">Ambiente Interno</span>
      </header>

      {/* Container de Mensagens */}
      <main className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4 max-w-4xl w-full mx-auto">
        {mensagens.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.tipo === 'usuario' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xl rounded-2xl px-5 py-3.5 text-sm leading-relaxed shadow-sm whitespace-pre-wrap ${
                msg.tipo === 'usuario'
                  ? 'bg-blue-600 text-white rounded-br-none'
                  : 'bg-slate-800 border border-slate-700 text-slate-200 rounded-bl-none'
              }`}
            >
              {msg.texto}
            </div>
          </div>
        ))}

        {/* Indicador de Digitação / Carregamento */}
        {carregando && (
          <div className="flex justify-start">
            <div className="bg-slate-800 border border-slate-700 text-slate-400 rounded-2xl rounded-bl-none px-5 py-3 text-sm flex items-center space-x-2">
              <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></span>
              <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:0.2s]"></span>
              <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:0.4s]"></span>
              <span className="ml-2 text-xs">Consultando base de conhecimento do Neo DB...</span>
            </div>
          </div>
        )}
        <div ref={fimDoChatRef} />
      </main>

      {/* Rodapé / Input de Pergunta */}
      <footer className="bg-slate-800 border-t border-slate-700 p-4">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto flex gap-3">
          <input
            type="text"
            value={pergunta}
            onChange={(e) => setPergunta(e.target.value)}
            placeholder="Digite sua dúvida corporativa (ex: limites de TED, políticas)..."
            className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition text-sm"
            disabled={carregando}
          />
          <button
            type="submit"
            disabled={carregando || !pergunta.trim()}
            className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-medium px-6 py-3 rounded-xl transition flex items-center justify-center shadow-lg text-sm"
          >
            Enviar
          </button>
        </form>
      </footer>
    </div>
  );
}