#version 330 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 textureCoordinate;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec3 texCoord;

void main() {
	vec4 worldPos = modelMatrix * vec4(position, 1.0);
	worldPos.w = 0.0f;
	gl_Position = projectionMatrix * viewMatrix * worldPos;
	texCoord = position;
}