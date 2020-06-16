#version 330 core

layout(location = 0) in vec2 squareVertices;
layout(location = 1) in vec4 color;
layout(location = 2) in mat4 modelMatrix;
layout(location = 6) in vec2 TexCoord;

uniform mat4 ViewProjMatrix;
uniform vec3 CameraRight;
uniform vec3 CameraUp;
uniform vec3 PartScale;

out vec2 UV;

void main()
{
	vec3 particlePosition = vec3(modelMatrix[3][0], modelMatrix[3][1], modelMatrix[3][2]);
	vec3 particleScale = vec3(PartScale.x, PartScale.y, PartScale.z);
	vec3 vertexPosition_worldspace = particlePosition + CameraRight * squareVertices.x * particleScale.x + CameraUp * squareVertices.y * particleScale.y;
	gl_Position = ViewProjMatrix * vec4(vertexPosition_worldspace, 1.0);

	UV = TexCoord;

}