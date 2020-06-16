#version 330 core

uniform vec4 diffuse;

out vec4 FragColor;

void main()
{
	if (diffuse.a < 0.01) {
		discard;
	}
    FragColor.xyz = diffuse.xyz;
}