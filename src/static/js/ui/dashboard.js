/**
 * DashboardUI (Presentation/View Layer)
 * 
 * Handles DOM manipulation and rendering. 
 * Completely decoupled from API fetching logic.
 */

export class DashboardUI {
    constructor(selectors) {
        this.container = document.querySelector(selectors.container);
        this.metrics = {
            total: document.querySelector(selectors.metrics.total),
            storage: document.querySelector(selectors.metrics.storage),
            requests: document.querySelector(selectors.metrics.requests)
        };

        // Templates
        this.spriteTemplate = (sprite) => {
            // Logic to get the latest preview
            const latestVersion = sprite.versions && sprite.versions.length > 0
                ? sprite.versions[sprite.versions.length - 1]
                : null;

            const imageUrl = latestVersion ? latestVersion.image_url : null;
            const versionCount = sprite.versions ? sprite.versions.length : 0;
            const previewContent = imageUrl
                ? `<img src="${imageUrl}" alt="${sprite.name}" style="max-width: 100%; max-height: 100%; object-fit: contain;">`
                : `<svg width="48" height="48" viewBox="0 0 24 24" stroke="var(--color-text-muted)" fill="none" stroke-width="1">
                        <circle cx="12" cy="12" r="10"></circle>
                        <text x="12" y="16" text-anchor="middle" font-size="8" fill="var(--color-text-muted)">No Img</text>
                   </svg>`;

            const tagsHtml = sprite.tags && sprite.tags.length > 0
                ? sprite.tags.map(tag => `<span class="tag">${tag}</span>`).join('')
                : `<span class="tag">Untagged</span>`;

            return `
            <div class="card sprite-card">
                <div class="sprite-preview">
                    ${previewContent}
                </div>
                <div class="sprite-meta">
                    <h3>${sprite.name}</h3>
                    <div style="display: flex; gap: 8px; margin-top: 8px; flex-wrap: wrap;">
                        ${tagsHtml}
                        <span class="tag">v${versionCount}</span>
                        <span class="tag">▶ ${sprite.play_count || 0}</span>
                    </div>
                </div>
                <div style="margin-top: 1rem; display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem;">
                     <button class="btn" style="font-size: 0.7rem; padding: 0.5rem 0.2rem;" 
                        onclick="window.app.loadSpriteInSimulator('${sprite.id}')">
                        Simulate
                     </button>
                     <button class="btn" style="font-size: 0.7rem; padding: 0.5rem 0.2rem;" 
                        onclick="window.navigate('library', { spriteId: '${sprite.id}' })">
                        Inspect
                     </button>
                     <button class="btn" style="font-size: 0.7rem; padding: 0.5rem 0.2rem;" 
                        onclick="window.navigate('editor', { spriteId: '${sprite.id}' })">
                        Edit
                     </button>
                </div>
            </div>
            `;
        };

        this.emptyTemplate = `
            <div style="text-align: center; color: var(--color-text-muted); grid-column: 1 / -1; padding: 2rem;">
                No sprites found. <button class="btn btn-primary" style="margin-left: 1rem;">Upload First Sprite</button>
            </div>
        `;
    }

    renderSprites(sprites) {
        if (!this.container) return;

        this.container.innerHTML = '';

        if (!sprites || sprites.length === 0) {
            this.container.innerHTML = this.emptyTemplate;
            return;
        }

        const html = sprites.map(sprite => this.spriteTemplate(sprite)).join('');
        this.container.innerHTML = html;

        // Update basic metric for total sprites
        if (this.metrics.total) {
            this.metrics.total.textContent = sprites.length;
        }
    }

    showError(error) {
        if (!this.container) return;
        this.container.innerHTML = `
            <div style="text-align: center; color: var(--color-danger); grid-column: 1 / -1; padding: 2rem;">
                Failed to load data: ${error.message}
            </div>
        `;
    }
}
