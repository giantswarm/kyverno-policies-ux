{{/*
Common labels
*/}}
{{- define "labels.common" -}}
application.giantswarm.io/team: {{ index .Chart.Annotations "application.giantswarm.io/team" | quote }}
{{- end -}}
