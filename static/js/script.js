document.addEventListener("DOMContentLoaded", () => {
	const downloadBtn = document.getElementById("download-btn");
	const urlInput = document.getElementById("playlist-url");
	const statusDiv = document.getElementById("status");
	const downloadsDiv = document.getElementById("downloads");

	// Função para listar os vídeos baixados
	function listDownloadedVideos() {
		fetch("/list-downloads")
			.then((response) => response.json())
			.then((data) => {
				downloadsDiv.innerHTML = ""; // Limpa a lista de vídeos

				if (data.videos && data.videos.length > 0) {
					data.videos.forEach((video) => {
						const videoLink = document.createElement("a");
						videoLink.href = `/downloads/${video.filename}`;
						videoLink.textContent = `Baixar: ${video.filename}`;
						videoLink.download = video.filename;
						downloadsDiv.appendChild(videoLink);

						const br = document.createElement("br");
						downloadsDiv.appendChild(br);
					});
				} else {
					downloadsDiv.textContent = "Nenhum vídeo baixado disponível.";
				}
			})
			.catch((error) => {
				console.error("Erro ao listar os vídeos baixados:", error);
				downloadsDiv.textContent = "Erro ao listar os vídeos.";
			});
	}

	// Chama a função para listar vídeos baixados ao carregar a página
	listDownloadedVideos();

	downloadBtn.addEventListener("click", () => {
		const url = urlInput.value.trim();
		if (!url) {
			statusDiv.textContent = "Por favor, insira uma URL válida.";
			return;
		}

		statusDiv.textContent = "Iniciando download...";
		downloadBtn.disabled = true;

		fetch("/download", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ url: url }),
		})
			.then((response) => {
				if (!response.ok) {
					return response.json().then((err) => {
						throw err;
					});
				}
				return response.json();
			})
			.then((data) => {
				statusDiv.textContent = data.message || "Download concluído!";
				listDownloadedVideos(); // Atualiza a lista de vídeos após o download
			})
			.catch((error) => {
				statusDiv.textContent = `Erro: ${error.error || "Ocorreu um erro desconhecido."}`;
				console.error("Error:", error);
			})
			.finally(() => {
				downloadBtn.disabled = false;
			});
	});
});
