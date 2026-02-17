/**
 * Simulation State (Domain)
 * 
 * Pure data structures representing the state of the simulation.
 * No DOM, no API calls, no rendering logic.
 */

export class SimulationState {
    constructor() {
        this.entities = [];
        this.camera = { x: 0, y: 0, scale: 1.0 };
        this.currentTime = 0;
    }

    addEntity(entity) {
        this.entities.push(entity);
    }

    clearEntities() {
        this.entities = [];
    }
}

/**
 * Simulation Logic (Domain Service)
 * 
 * Pure function to update state based on delta time.
 */
export class SimulationLogic {
    static update(state, dt) {
        state.currentTime += dt;

        state.entities.forEach(entity => {
            if (entity.update) {
                entity.update(dt);
            }
            // Basic physics (velocity) if present
            if (entity.vx) entity.x += entity.vx * dt;
            if (entity.vy) entity.y += entity.vy * dt;
        });

        return state;
    }
}
