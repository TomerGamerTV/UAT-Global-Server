<template>
  <div v-if="show" class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-dialog" @click.stop>
      <div class="modal-content notification-dialog">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="fas fa-tools"></i>
            Manual Skill Purchase Required
          </h5>
          <button type="button" class="btn-close" @click="handleCancel" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="notification-content">
            <div class="notification-icon">
              <i class="fas fa-hand-paper"></i>
            </div>
            <div class="notification-text">
              <p class="notification-message">
                Please learn skills manually in the game, then press the <strong>Confirm</strong> button when you're done.
              </p>
              <p class="notification-hint">
                The bot will continue automatically after you complete the skill purchase.
              </p>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="handleCancel">
            Cancel
          </button>
          <button type="button" class="btn btn-primary" @click="handleConfirm">
            I'm Done - Continue
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ManualSkillNotificationModal',
  props: {
    show: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:show', 'confirm', 'cancel'],
  methods: {
    handleConfirm() {
      this.$emit('confirm');
      this.$emit('update:show', false);
    },
    handleCancel() {
      this.$emit('cancel');
      this.$emit('update:show', false);
    },
    handleOverlayClick() {
      // Don't close when clicking overlay - require explicit button click
    }
  }
};
</script>

<style scoped>
/* Modal overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-dialog {
  max-width: 500px;
  width: 90%;
  margin: 0;
}

/* Modern notification dialog styling */
.notification-dialog {
  border-radius: 12px;
  border: none;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.notification-dialog .modal-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px 12px 0 0;
  border: none;
  padding: 1.5rem;
}

.notification-dialog .modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.notification-dialog .modal-title i {
  margin-right: 0.5rem;
  color: #ffd700;
}

.notification-dialog .btn-close {
  filter: invert(1);
  opacity: 0.8;
}

.notification-dialog .btn-close:hover {
  opacity: 1;
}

.notification-dialog .modal-body {
  padding: 2rem;
  background: #f8f9fa;
}

.notification-content {
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
}

.notification-icon {
  flex-shrink: 0;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
}

.notification-text {
  flex: 1;
}

.notification-message {
  font-size: 1.1rem;
  color: #2c3e50;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.notification-hint {
  font-size: 0.95rem;
  color: #6c757d;
  margin: 0;
  font-style: italic;
}

.notification-dialog .modal-footer {
  background: white;
  border-top: 1px solid #e9ecef;
  padding: 1.5rem;
  border-radius: 0 0 12px 12px;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.notification-dialog .btn {
  padding: 0.75rem 1.5rem;
  font-weight: 500;
  border-radius: 8px;
  border: none;
  transition: all 0.2s ease;
}

.notification-dialog .btn-secondary {
  background: #6c757d;
  color: white;
}

.notification-dialog .btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-1px);
}

.notification-dialog .btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.notification-dialog .btn-primary:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

/* Ensure modal appears on top */
#manual-skill-notification-modal.modal {
  z-index: 1070;
}

#manual-skill-notification-modal .modal-dialog {
  z-index: 1071;
}

/* Animation for the notification icon */
.notification-icon {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

/* Responsive design */
@media (max-width: 576px) {
  .notification-content {
    flex-direction: column;
    text-align: center;
  }
  
  .notification-icon {
    align-self: center;
  }
}
</style> 