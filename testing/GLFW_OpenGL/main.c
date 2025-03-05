#include <GLFW/glfw3.h>
#include <stdio.h>
#include <math.h>


double targetFrameTime = 1.0 / 60.0; // 60 FPS


void drawTriangle(float angle) {
    glPushMatrix();
    glRotatef(angle, 0.0f, 0.0f, 1.0f);
    
    glBegin(GL_TRIANGLES);
    glColor3f(1.0f, 0.0f, 0.0f);
    glVertex2f(-0.5f, -0.5f);
    glColor3f(0.0f, 1.0f, 0.0f);
    glVertex2f(0.5f, -0.5f);
    glColor3f(0.0f, 0.0f, 1.0f);
    glVertex2f(0.0f, 0.5f);
    glEnd();
    
    glPopMatrix();
}

int main(void) {
    if (!glfwInit()) {
        return -1;
    }

    GLFWwindow* window = glfwCreateWindow(800, 600, "Rotating Triangle", NULL, NULL);
    if (!window) {
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window);
    
    float angle = 0.0f;
    float rotationSpeed = 45.0f; // 45 degrees per second
    double lastTime = glfwGetTime();

    while (!glfwWindowShouldClose(window)) {
        double currentTime = glfwGetTime();
        float deltaTime = (float)(currentTime - lastTime);
        lastTime = currentTime;
        
        angle += rotationSpeed * deltaTime;
        float time = (float)currentTime;
        
        // Color-shifting background
        float r = (sinf(time * 0.5f) + 1.0f) * 0.25f;
        float g = (sinf(time * 0.5f + 2.0f) + 1.0f) * 0.25f;
        float b = (sinf(time * 0.5f + 4.0f) + 1.0f) * 0.25f;
        
        glClearColor(r, g, b, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);
        
        drawTriangle(angle);

        double frameTime = glfwGetTime() - currentTime;
        if (frameTime < targetFrameTime) {
            double sleepTime = targetFrameTime - frameTime;
            glfwWaitEventsTimeout(sleepTime);
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}
