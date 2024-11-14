import yt_dlp
import os
import logging

def download_playlist(url):
    downloaded_videos = []  # Lista para armazenar informações dos vídeos baixados
    
    try:
        # Verifica se o diretório 'downloads' existe, caso contrário, cria-o
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'logger': logging.getLogger(),
            'progress_hooks': [lambda d: logging.info(f"Baixando: {d['filename']}") if d['status'] == 'downloading' else None],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            if 'entries' in info_dict:
                for entry in info_dict['entries']:
                    try:
                        video_url = entry['webpage_url']
                        result = ydl.download([video_url])
                        # Adiciona os detalhes do vídeo baixado à lista
                        downloaded_videos.append({
                            'title': entry.get('title', 'Título desconhecido'),
                            'filename': f"{entry.get('title', 'Título desconhecido')}.mp4"
                        })
                    except Exception as e:
                        logging.error(f"Erro ao baixar vídeo {entry.get('title', 'desconhecido')}: {str(e)}")
            else:
                raise ValueError("Não foi possível obter os vídeos da playlist. Verifique se a URL está correta e a playlist é pública.")
    
    except Exception as e:
        logging.error(f"Erro ao processar a playlist: {str(e)}")
        raise

    return downloaded_videos  # Retorna a lista de vídeos baixados para o frontend
