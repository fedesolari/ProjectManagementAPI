OK = 0
TICKET_NOT_FOUND = 1
TICKET_NOT_CREATED = 2
TITLE_TOO_LONG = 3
DESCRIPTION_TOO_LONG = 4
NOT_VALID_PRIORITY = 5
NOT_VALID_SEVERITY = 6
NOT_VALID_STATE = 7
CLIENT_NOT_FOUND = 8
NO_RESOURCE_ASSIGNED = 9
NONE_PARAMETER = 10
INVALID_PRODUCT_VERSION_ID = 11
STATE_CHANGE_TO_NEW = 12
TASK_NOT_CREATED = 13
TASK_ALREADY_ASSIGNED = 14


response_code_map = {
    OK: "ok",
    TICKET_NOT_FOUND: "No se encontró el ticket solicitado.",
    TICKET_NOT_CREATED: "No se pudo crear el ticket.",
    TITLE_TOO_LONG: "El título del ticket se excedió del límite.",
    DESCRIPTION_TOO_LONG: "La descripción del ticket se excedió del límite.",
    NOT_VALID_PRIORITY: "La prioridad seleccionada no es válida.",
    NOT_VALID_SEVERITY: "La severidad seleccionada no es válida.",
    NOT_VALID_STATE: "El estado selecccionado no es válido.",
    CLIENT_NOT_FOUND: "No se encontró el cliente solicitado.",
    NO_RESOURCE_ASSIGNED: "Se debe asociar un recurso para cambiar el estado del ticket.",
    NONE_PARAMETER: "Se encontraron parametros que son nulos.",
    INVALID_PRODUCT_VERSION_ID: "La version de producto seleccionada no es válida.",
    STATE_CHANGE_TO_NEW: "No se puede cambiar el estado de un ticket a NEW.",
    TASK_NOT_CREATED: "No se pudo asignar la tarea al ticket.",
    TASK_ALREADY_ASSIGNED: "La tarea ya se encuentra asignada al ticket."
}
