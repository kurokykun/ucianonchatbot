class MatchMaker:
    def __init__(self):
        self.queue = {"chicos": [], "chicas": []}
        self.active_chats = {}

    def add_to_queue(self, user_id, preference):
        """Añade un usuario a la cola según su preferencia (género)."""
        if preference not in self.queue:
            raise ValueError("Preferencia de género inválida, debe ser 'chicos' o 'chicas'")
        self.queue[preference].append(user_id)

    def find_match(self, user_id, preferred_gender):
        """Intenta emparejar al usuario con alguien del género preferido."""
        # Validar que el género preferido sea válido
        if preferred_gender not in self.queue:
            raise ValueError("Género preferido inválido, debe ser 'chicos' o 'chicas'")
        
        # Determinar el género opuesto
        opposite_gender = "chicas" if preferred_gender == "chicos" else "chicos"

        # Primero intentar emparejar con alguien del género opuesto
        if self.queue[opposite_gender]:
            # Buscar al primer usuario disponible en la cola del género opuesto
            partner_id = self.queue[opposite_gender].pop(0)
            
            # Verificar que no se empareje con el mismo usuario
            if partner_id == user_id:
                # Si el partner es el mismo usuario, no lo emparejamos y volvemos a la cola
                self.queue[opposite_gender].insert(0, partner_id)  # Regresamos a la cola
                return None
            
            # Eliminar al usuario de la cola correspondiente (si está presente)
            if user_id in self.queue["chicos"]:
                self.queue["chicos"].remove(user_id)
            elif user_id in self.queue["chicas"]:
                self.queue["chicas"].remove(user_id)

            # Iniciar la conversación
            self.start_conversation(user_id, partner_id)
            
            return partner_id

         # Si no hay nadie del género opuesto, proceder con el emparejamiento dentro del mismo género
        if self.queue[preferred_gender]:
            # Buscar al primer usuario disponible en la cola
            partner_id = self.queue[preferred_gender].pop(0)
            
            # Verificar que no se empareje con el mismo usuario
            if partner_id == user_id:
                # Si el partner es el mismo usuario, no lo emparejamos y volvemos a la cola
                self.queue[preferred_gender].insert(0, partner_id)  # Regresamos a la cola
                return None

            # Eliminar al usuario de la cola correspondiente, solo si está presente
            if user_id in self.queue["chicos"]:
                self.queue["chicos"].remove(user_id)
            elif user_id in self.queue["chicas"]:
                self.queue["chicas"].remove(user_id)

            # Iniciar la conversación
            self.start_conversation(user_id, partner_id)
            
            return partner_id

        return None

    def remove_from_queue(self, user_id):
        """Elimina al usuario de la cola de espera."""
        for gender in self.queue:
            if user_id in self.queue[gender]:
                self.queue[gender].remove(user_id)
                break

    def start_conversation(self, user_id, partner_id):
        """Inicia una conversación entre dos usuarios."""
        self.active_chats[user_id] = partner_id
        self.active_chats[partner_id] = user_id

    def get_partner(self, user_id):
        """Obtiene el compañero de conversación del usuario."""
        return self.active_chats.get(user_id)

    def end_conversation(self, user_id):
        """Finaliza la conversación del usuario."""
        partner_id = self.active_chats.pop(user_id, None)
        if partner_id:
            self.active_chats.pop(partner_id, None)
        return partner_id
