#version 330

uniform sampler2D modelTexture;
uniform vec4 diffuse;
uniform bool UsesTexture;

void main() {
	gl_FragColor = diffuse;
}