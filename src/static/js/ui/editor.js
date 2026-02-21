/**
 * Animation Editor UI
 * Handles the creation and modification of animation sequences.
 */
export class EditorUI {
    constructor(spriteService) {
        this.spriteService = spriteService;
        this.currentSprite = null;
        this.selectedFrames = [];
    }

    async init() {
        console.log("Animation Editor Initialized");
    }

    async loadSprite(spriteId) {
        try {
            this.currentSprite = await this.spriteService.getSprite(spriteId);
            this.render();
        } catch (error) {
            console.error("Failed to load sprite for editor:", error);
        }
    }

    render() {
        const container = document.getElementById('editor-view');
        if (!container) return;

        if (!this.currentSprite) {
            container.innerHTML = `
                <div style="text-align: center; padding: 4rem;">
                    <h2>No Sprite Selected</h2>
                    <p>Select a sprite from the dashboard to start editing animations.</p>
                    <button class="btn btn-primary" onclick="window.navigate('dashboard')" style="margin-top: 1rem;">Go to Dashboard</button>
                </div>
            `;
            return;
        }

        const latestVersion = this.currentSprite.versions && this.currentSprite.versions.length > 0
            ? this.currentSprite.versions[this.currentSprite.versions.length - 1]
            : null;

        container.innerHTML = `
            <header class="header animate-fade-in">
                <div class="page-title">
                    <h1>Animation Editor</h1>
                    <p>Editing: <strong>${this.currentSprite.name}</strong></p>
                </div>
                <div class="actions">
                    <button class="btn" onclick="window.navigate('dashboard')">Back</button>
                    <button class="btn btn-primary" onclick="window.app.editor.saveAnimations()">Save Changes</button>
                </div>
            </header>

            <div style="display: grid; grid-template-columns: 350px 1fr; gap: var(--spacing-lg); height: calc(100vh - 200px);">
                <!-- Frame Selection -->
                <div class="card" style="display: flex; flex-direction: column; overflow: hidden;">
                    <h3 style="margin-bottom: var(--spacing-md); padding: 0 var(--spacing-sm);">Available Frames</h3>
                    <div id="editor-frames-grid" style="flex: 1; overflow-y: auto; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; padding: 8px;">
                        ${this._renderAvailableFrames(latestVersion)}
                    </div>
                </div>

                <!-- Sequence Builder -->
                <div class="card" style="display: flex; flex-direction: column; overflow: hidden;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--spacing-md);">
                        <h3>Animation Sequences</h3>
                        <button class="btn" style="font-size: 0.8rem; padding: 0.25rem 0.75rem;" onclick="window.app.editor.addNewSequence()">+ New Sequence</button>
                    </div>
                    <div id="sequences-container" style="flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: var(--spacing-md);">
                        ${this._renderSequences(latestVersion)}
                    </div>
                </div>
            </div>
        `;
    }

    _renderAvailableFrames(version) {
        if (!version || !version.image_url) return '<p>No frames available.</p>';

        // This is a simplification. Ideally we'd use the individual frame URLs if they exist.
        // For now, let's assume we use the indices.
        let html = '';
        // If we have sliced frames, show them.
        // The version.animations might contain frame info, but we likely want the raw frames.
        // Let's use a dummy loop if we don't have meta.
        const frameW = version.metadata.frame_w || 0;
        const frameH = version.metadata.frame_h || 0;

        // In a real scenario, we'd fetch all frames. 
        // For the MVP, let's look at the animations shared frames.
        const frames = [];
        if (version.animations) {
            version.animations.forEach(a => a.frames.forEach(f => {
                if (!frames.find(ex => ex.index === f.index)) frames.push(f);
            }));
        }

        if (frames.length === 0) return '<p>No sliced frames found. Ensure the sprite was uploaded with grid settings.</p>';

        return frames.map(f => `
            <div class="frame-item" onclick="window.app.editor.addFrameToActiveSequence(${f.index})" 
                 style="background: rgba(0,0,0,0.2); border-radius: 4px; padding: 4px; cursor: pointer; border: 1px solid transparent; transition: all 0.2s;"
                 onmouseover="this.style.borderColor='var(--color-primary)'" 
                 onmouseout="this.style.borderColor='transparent'">
                <img src="${f.image_location}" style="width: 100%; height: auto; display: block; image-rendering: pixelated;">
                <span style="font-size: 0.6rem; color: var(--color-text-muted); display: block; text-align: center;">ID: ${f.index}</span>
            </div>
        `).join('');
    }

    _renderSequences(version) {
        if (!version || !version.animations || version.animations.length === 0) {
            return '<p style="text-align: center; color: var(--color-text-muted); padding: 2rem;">No sequences defined. Create one to start.</p>';
        }

        return version.animations.map((anim, animIdx) => `
            <div class="sequence-card" style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 8px; padding: var(--spacing-md);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <input type="text" value="${anim.name}" onchange="window.app.editor.updateSequenceName(${animIdx}, this.value)"
                           style="background: transparent; border: none; border-bottom: 1px solid transparent; color: var(--color-text-main); font-weight: 600; outline: none;"
                           onfocus="this.style.borderBottomColor='var(--color-primary)'" onblur="this.style.borderBottomColor='transparent'">
                    <button class="btn" style="padding: 2px 8px; color: var(--color-danger); background: transparent;" onclick="window.app.editor.removeSequence(${animIdx})">
                        &times;
                    </button>
                </div>
                <div class="sequence-frames" style="display: flex; gap: 8px; overflow-x: auto; padding-bottom: 8px;">
                    ${anim.frames.map((f, fIdx) => `
                        <div style="position: relative; flex: 0 0 60px;">
                            <img src="${f.image_location}" style="width: 60px; height: 60px; object-fit: contain; background: black; border-radius: 4px;">
                            <input type="number" value="${f.duration_ms || 100}" onchange="window.app.editor.updateFrameDuration(${animIdx}, ${fIdx}, this.value)"
                                   style="width: 100%; font-size: 0.75rem; background: var(--color-bg-card); border: 1px solid var(--border-color); color: var(--color-text-main); border-radius: 2px; text-align: center; margin-top: 4px;">
                            <button onclick="window.app.editor.removeFrameFromSequence(${animIdx}, ${fIdx})"
                                    style="position: absolute; top: -4px; right: -4px; background: var(--color-danger); color: white; border: none; border-radius: 50%; width: 16px; height: 16px; font-size: 10px; cursor: pointer; display: flex; align-items: center; justify-content: center;">
                                &times;
                            </button>
                        </div>
                    `).join('')}
                    <div style="flex: 0 0 60px; height: 60px; border: 2px dashed var(--border-color); border-radius: 4px; display: flex; align-items: center; justify-content: center; color: var(--color-text-muted); font-size: 1.5rem;">
                        +
                    </div>
                </div>
            </div>
        `).join('');
    }

    // Logic methods
    addNewSequence() {
        if (!this.currentSprite) return;
        const latestVersion = this.currentSprite.versions[this.currentSprite.versions.length - 1];
        if (!latestVersion.animations) latestVersion.animations = [];
        latestVersion.animations.push({
            name: `Animation ${latestVersion.animations.length + 1}`,
            frames: [],
            loop: true,
            fps: 10
        });
        this.render();
    }

    updateSequenceName(animIdx, name) {
        const latestVersion = this.currentSprite.versions[this.currentSprite.versions.length - 1];
        latestVersion.animations[animIdx].name = name;
    }

    removeSequence(animIdx) {
        const latestVersion = this.currentSprite.versions[this.currentSprite.versions.length - 1];
        latestVersion.animations.splice(animIdx, 1);
        this.render();
    }

    addFrameToActiveSequence(frameIndex) {
        if (!this.currentSprite) return;
        const latestVersion = this.currentSprite.versions[this.currentSprite.versions.length - 1];
        if (!latestVersion.animations || latestVersion.animations.length === 0) {
            this.addNewSequence();
        }

        const activeAnim = latestVersion.animations[latestVersion.animations.length - 1];

        // Find the image_location for this index
        let frameData = null;
        latestVersion.animations.forEach(a => a.frames.forEach(f => {
            if (f.index === frameIndex) frameData = f;
        }));

        if (frameData) {
            activeAnim.frames.push({
                index: frameData.index,
                image_location: frameData.image_location,
                duration_ms: 100
            });
            this.render();
        }
    }

    updateFrameDuration(animIdx, frameIdx, duration) {
        const latestVersion = this.currentSprite.versions[this.currentSprite.versions.length - 1];
        latestVersion.animations[animIdx].frames[frameIdx].duration_ms = parseInt(duration);
    }

    removeFrameFromSequence(animIdx, frameIdx) {
        const latestVersion = this.currentSprite.versions[this.currentSprite.versions.length - 1];
        latestVersion.animations[animIdx].frames.splice(frameIdx, 1);
        this.render();
    }

    async saveAnimations() {
        if (!this.currentSprite) return;
        const latestVersion = this.currentSprite.versions[this.currentSprite.versions.length - 1];

        try {
            console.log("Saving animations to backend:", latestVersion.animations);
            await this.spriteService.updateAnimations(this.currentSprite.id, latestVersion.animations);
            alert("Animations saved successfully!");
        } catch (error) {
            console.error("Failed to save animations:", error);
            alert("Failed to save: " + error.message);
        }
    }
}
