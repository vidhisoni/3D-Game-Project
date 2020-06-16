#version 330 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 textureCoordinate;

out vec3 normals;
out vec3 worldPos;
out vec2 texCoord;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main() {
	worldPos = vec3(modelMatrix * vec4(position, 1.0f));
	normals = mat3(transpose(inverse(modelMatrix))) * normal;
	texCoord = textureCoordinate;

	gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0f);
}