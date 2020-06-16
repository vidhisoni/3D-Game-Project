#version 330 core

in vec3 texCoord;

uniform samplerCube cubeMap;
uniform vec4 diffuse;
uniform bool UsesTexture;

void main() {
	if (UsesTexture) {
		gl_FragColor = texture(cubeMap, texCoord);
	}
	else {
		gl_FragColor = diffuse;
	}
}